"""10 mm acrylic Tifa derivative. Millimetres. Whole sheet profiles -> DXF/SVG/STL.
Run this file with CadQuery; manufacturing exports are in panel_exports.py.
"""
from pathlib import Path
import json, math
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'cad/speaker_parameters.json').read_text())
V=cq.Vector

def box(x,y,z,dx,dy,dz):return cq.Solid.makeBox(dx,dy,dz,V(x,y,z))
def cyl(r,h,x,y,z,axis=(0,1,0)):return cq.Solid.makeCylinder(r,h,V(x,y,z),V(*axis))
def union(shapes):
    s=shapes[0]
    for q in shapes[1:]:s=s.fuse(q)
    return s.clean()
def compound(shapes):return cq.Compound.makeCompound(list(shapes))
def place(s,p):return s.located(cq.Location(cq.Plane(tuple(p['origin']),tuple(p['xdir']),tuple(p['normal']))))
def local(p,point):return cq.Plane(tuple(p['origin']),tuple(p['xdir']),tuple(p['normal'])).toLocalCoords(V(*point))
def panel_shape(p):
    s=box(0,0,0,*p['size'],10)
    for cut in p['rect_cuts']:s=s.cut(box(*cut[:2],-1,*cut[2:],12))
    for h in p['holes']:s=s.cut(cyl(h['diameter']/2,12,h['u'],h['v'],-1,(0,0,1)))
    return s.clean()

def geometry(D):
    W,H,t,g=P['width'],P['height'],P['sheet_thickness'],P['gasket_compressed']
    assert t==10 and W==220 and H==380, 'This manufacturing layout is for 220 x 380, 10 mm stock.'
    wz,tz,pz=P['woofer_centre_z'],P['tweeter_centre_z'],P['port_centre_z']
    panels={}; fittings={}; bolts=[]; inserts=[]
    def panel(name,size,origin,xdir,normal,exterior):
        panels[name]={'size':list(size),'origin':list(origin),'xdir':list(xdir),'normal':list(normal),'exterior':exterior,'holes':[],'rect_cuts':[]}
    panel('front',(W,H),(-W/2,t,0),(1,0,0),(0,-1,0),10)
    panel('rear',(W,H),(-W/2,D,0),(1,0,0),(0,-1,0),0)
    for side,x,ext in [('left',-W/2,0),('right',W/2-t,10)]:
        panel(side,(D-2*t-2*g,H-2*t-2*g),(x,t+g,t+g),(0,1,0),(1,0,0),ext)
    for name,z,ext in [('bottom',0,0),('top',H-t,10)]:
        panel(name,(W,D-2*t-2*g),(-W/2,t+g,z),(1,0,0),(0,0,1),ext)
    panel('brace',(199,D-22),(-99.5,11,250),(1,0,0),(0,0,1),10)
    br=panels['brace'];br['rect_cuts'].append([30,30,139,D-82])
    # Corner notches pass the rails; the shallow front notch clears the woofer flange.
    for u in [-1,181]:
        for v in [-1,D-40]:br['rect_cuts'].append([u,v,19,19])
    br['rect_cuts'].append([49.5,-1,100,7])
    def hole(panel_name,pt,diameter=4.5,purpose='M3 fixing'):
        p=panels[panel_name];q=local(p,pt)
        p['holes'].append({'u':q.x,'v':q.y,'diameter':diameter,'purpose':purpose})
    def screw(label,start,axis,length,receiver=None):
        bolts.append({'label':label,'start':list(start),'axis':list(axis),'length':length,'receiver':receiver})
    def pilot(name,pt,axis,depth=5):
        fittings[name]=fittings[name].cut(cyl(2.1,depth,*pt,axis)).clean()
        inserts.append({'part':name,'entry':list(pt),'axis':list(axis),'depth':depth,'length':4})
    # Eight L rails. Two lengths per corner; upper rails have integral brace ledges.
    for sx in [-1,1]:
        for rear in [False,True]:
            def tx(s):
                if sx==1:s=s.mirror('YZ')
                if rear:s=s.mirror('XZ',(0,D/2,0))
                return s
            yface=D-10.5 if rear else 10.5;ydir=-1 if rear else 1
            yy=D-21.5 if rear else 21.5
            for upper in [False,True]:
                z0=190 if upper else 10.5;z1=369.5 if upper else 190
                s=union([box(-100,10.5,z0,18,8,z1-z0),box(-100,10.5,z0,8,18,z1-z0)])
                if upper:s=s.fuse(box(-92,14,244,30,14,6)).clean()
                name=f'rail_{"right" if sx==1 else "left"}_{"rear" if rear else "front"}_{"upper" if upper else "lower"}'
                fittings[name]=tx(s)
                for z in ([225,350] if upper else [30,105]):
                    pilot(name,(sx*91,yface,z),(0,ydir,0))
                    face='rear' if rear else 'front';hole(face,(sx*91,yface,z))
                    screw('panel_to_rail',(sx*91,D+1.5 if rear else -1.5,z),(0,ydir,0),16,name)
                for z in ([225,340] if upper else [50,155]):
                    pilot(name,(sx*100,yy,z),(-sx,0,0))
                    hole('right' if sx==1 else 'left',(sx*100,yy,z))
                    screw('panel_to_rail',(sx*111.5,yy,z),(-sx,0,0),16,name)
                cap='top' if upper else 'bottom';z=369.5 if upper else 10.5;zd=-1 if upper else 1
                ycap=D-19.5 if rear else 19.5
                pilot(name,(sx*96,ycap,z),(0,0,zd));hole(cap,(sx*96,ycap,z))
                screw('cap_to_rail',(sx*96,ycap,H+1.5 if upper else -1.5),(0,0,zd),16,name)
                if upper:
                    by=D-24 if rear else 24
                    pilot(name,(sx*70,by,250),(0,0,-1));hole('brace',(sx*70,by,250))
                    screw('brace_to_rail',(sx*70,by,261.5),(0,0,-1),16,name)
    # Adapters: circular panel holes and original seating planes. Radial foam seals
    # the 0.5 mm annular fit gap. Rear flange clips avoid rails and roof.
    driver_holes={};adapter_mounts={}
    for name,z,outer,opening,seat,pcd,flange,fixpcd in [
        ('woofer',wz,176,145,3.6,165,200,192),('tweeter',tz,100,73,3,88.5,126,116)]:
        hole('front',(0,0,z),outer+1,name+' adapter opening')
        nose=cyl(outer/2,10-seat,0,seat,z)
        neck=cyl(outer/2,6.5,0,10,z)
        lip=cyl(flange/2,6,0,10.5,z)
        clip=box(-81,-5,0,162,30,500) if name=='woofer' else box(-100,-5,0,200,30,369)
        s=union([nose,neck.intersect(clip),lip.intersect(clip)])
        s=s.cut(cyl(opening/2,20,0,0,z))
        if name=='tweeter':s=s.cut(box(-40.9,0,z-6.5,81.8,22,13))
        fittings[name+'_adapter']=s.clean();driver_holes[name]=[];adapter_mounts[name]=[]
        for a in [45,135,225,315]:
            angle=math.radians(a);x=pcd/2*math.cos(angle);zz=z+pcd/2*math.sin(angle)
            pilot(name+'_adapter',(x,seat,zz),(0,1,0),7)
            screw(name+'_driver',(x,-.5 if name=='woofer' else -1,zz),(0,1,0),10,name+'_adapter')
            driver_holes[name].append([x,zz])
            x=fixpcd/2*math.cos(angle);zz=z+fixpcd/2*math.sin(angle)
            hole('front',(x,0,zz));pilot(name+'_adapter',(x,10.5,zz),(0,1,0))
            screw(name+'_adapter_to_panel',(x,-1.5,zz),(0,1,0),16,name+'_adapter')
            adapter_mounts[name].append([x,zz])
    woo=fittings.pop('woofer_adapter')
    fittings['woofer_adapter_lower']=woo.intersect(box(-110,0,wz-110,220,25,109.9)).clean()
    fittings['woofer_adapter_upper']=woo.intersect(box(-110,0,wz+.1,220,25,110)).clean()
    for rec in inserts:
        if rec['part']=='woofer_adapter':rec['part']='woofer_adapter_lower' if rec['entry'][2]<wz else 'woofer_adapter_upper'
    for rec in bolts:
        if rec['receiver']=='woofer_adapter':rec['receiver']='woofer_adapter_lower' if rec['start'][2]<wz else 'woofer_adapter_upper'
    # Port flange rests outside the rear sheet on a 0.5 mm gasket. Mouth is D+3.5.
    r=P['port_bore']/2;L=P['port_length'];R=14;mouth=D+3.5
    outer=(cq.Workplane('XZ').moveTo(0,-L).lineTo(0,0).lineTo(48,0).lineTo(48,-3)
           .lineTo(36.25,-3).lineTo(36.25,-14).lineTo(r+2,-30).lineTo(r+2,-L).close().revolve(360,(0,0),(0,1)).val())
    inner=(cq.Workplane('XZ').moveTo(0,-L-1).lineTo(r,-L-1).lineTo(r,-R)
           .threePointArc((r+R-R/math.sqrt(2),-R+R/math.sqrt(2)),(r+R,0))
           .lineTo(r+R,1).lineTo(0,1).close().revolve(360,(0,0),(0,1)).val())
    def portplace(s):return s.rotate((0,0,0),(1,0,0),-90).translate((0,mouth,pz))
    outer=portplace(outer);inner=portplace(inner)
    portouter=outer
    port=portouter.cut(inner).clean();hole('rear',(0,D,pz),73,'port spigot')
    for a in [45,135,225,315]:
        x=44*math.cos(math.radians(a));z=pz+44*math.sin(math.radians(a))
        hole('rear',(x,D,z));port=port.cut(cyl(1.7,5,x,D-1,z))
        screw('port_flange_nut',(x,mouth+1.5,z),(0,-1,0),20)
    fittings['bass_reflex_port']=port.clean()
    # Standard purchased crossover stand-offs, not additional printed brackets.
    for x in [-15,15]:hole('rear',(x,D,225),8,'binding post')
    spacers=[]
    for x in [-50,50]:
        for z in [110,180]:
            hole('rear',(x,D,z));spacers.append(cyl(3,20,x,D-30,z).cut(cyl(1.7,22,x,D-31,z)))
            screw('crossover_spacer_rear',(x,D+1.5,z),(0,-1,0),16)
            screw('crossover_board',(x,D-32,z),(0,1,0),6)
    # Approximate driver solids and crossover clearance envelope; not vendor CAD.
    basket=cq.Solid.makeCone(71,45,54,V(0,7.6,wz),V(0,1,0)).cut(cq.Solid.makeCone(69,43,54,V(0,7.6,wz),V(0,1,0)))
    motor=cyl(42.5,25,0,55.3,wz)
    cone=cq.Solid.makeCone(64,18,23,V(0,3.6,wz),V(0,1,0)).cut(cq.Solid.makeCone(62,16,23,V(0,3.6,wz),V(0,1,0)))
    flange=cyl(88,4.1,0,-.5,wz).cut(cyl(63,6,0,-1,wz))
    proxies={'woofer':union([flange,basket,motor,cone]),'tweeter':union([cyl(50,4,0,-1,tz),cyl(35,26.7,0,3,tz),box(-40.65,3,tz-6,81.3,7,12)]),
        'crossover':box(-60,D-85,100,120,55,90),'spacers':compound(spacers)}
    shapes={n:place(panel_shape(p),p) for n,p in panels.items()}
    air=box(-100,10,10,200,D-20,360)
    air=air.fuse(cyl(72.5,6.4,0,3.6,wz)).fuse(cyl(36.5,7,0,3,tz)).fuse(box(-40.9,3,tz-6.5,81.8,7,13)).clean()
    ledger={'gross_cavity_and_driver_wells_litres':air.Volume()/1e6}
    start=air.Volume()
    for s in [*fittings.values(),shapes['brace']]:air=air.cut(s).clean()
    ledger['printed_fittings_and_acrylic_brace_litres']=(start-air.Volume())/1e6
    deductions=[('port_duct_air',portouter),('woofer_estimate',proxies['woofer']),('tweeter_estimate',proxies['tweeter']),
        ('crossover_material_estimate',box(-60,D-30-120000/(120*90),100,120,120000/(120*90),90)),
        ('spacers',proxies['spacers']),('wiring_allowance',box(75,D-15,105,5,5,100)),
        ('hardware_allowance',box(-25,D-45,270,10,10,100))]
    for name,s in deductions:
        before=air.Volume();air=air.cut(s).clean();ledger[name+'_litres']=(before-air.Volume())/1e6
    ledger['nominal_net_litres']=air.Volume()/1e6
    meta={'dimensions_mm':[W,D,H],'thickness_mm':10,'volume':ledger,'bolts':bolts,'inserts':inserts,
        'driver_holes':driver_holes,'adapter_mounts':adapter_mounts,'port_mouth_y':mouth,
        'port_inlet_to_front_wall_mm':mouth-L-10,'port_inlet_edge_to_floor_mm':pz-r-10,'gasket_mm':g}
    return panels,shapes,fittings,proxies,air,meta

def model():
    # Keep the released whole-panel dimensions. The continuous port gives ~16.115 L.
    result=geometry(P['depth'])
    assert abs(result[-1]['volume']['nominal_net_litres']-P['target_net_litres'])<.03
    return result

if __name__=='__main__':
    from panel_exports import export_all
    export_all(model())
