"""Exact sheet profiles, prototype seams, and manufacturing exports."""
from speaker_assembly import *
from copy import deepcopy
import csv, shutil
import trimesh, ezdxf

def prototype(data):
    profiles,fullpanels,original,proxies,air,meta=data
    ps=deepcopy(profiles);fit=dict(original);tiles={};splices={};extra=[];new_inserts=[];nut_envelopes={};tile_info={}
    def splice(panel_name,u,v,kind,along='u'):
        p=ps[panel_name];cross=kind=='cross';a,b=(28,28) if cross else ((28,16) if along=='u' else (16,28))
        centres=[(-8,-8),(-8,8),(8,-8),(8,8)] if cross else ([(-8,0),(8,0)] if along=='u' else [(0,-8),(0,8)])
        out=p['exterior'];sign=1 if out==10 else -1
        s=box(u-a/2,v-b/2,10 if sign==1 else -4,a,b,4)
        # The strap footprint must lie entirely on solid panel material.
        test=box(u-a/2,v-b/2,0,a,b,10)
        assert abs(test.intersect(panel_shape(p)).Volume()-a*b*10)<.05,(panel_name,u,v,'strap over opening')
        number=len(splices)+1;name=f'splice_{number:02d}_{panel_name}_{kind}'
        for du,dv in centres:
            uu,vv=u+du,v+dv
            p['holes'].append({'u':uu,'v':vv,'diameter':4.5,'purpose':'PROTOTYPE ONLY splice'})
            s=s.cut(cyl(1.7,8,uu,vv,-5 if sign==-1 else 9,(0,0,1)))
            plane=cq.Plane(tuple(p['origin']),tuple(p['xdir']),tuple(p['normal']))
            start=plane.toWorldCoords(V(uu,vv,out+sign*5.5));axis=V(*p['normal']).multiply(-sign)
            receiver=None
            if panel_name=='front' and abs(uu-110)>90:
                xyz=plane.toWorldCoords(V(uu,vv,0));receiver=f'rail_{"left" if xyz.x<0 else "right"}_front_{"lower" if xyz.z<190 else "upper"}'
                point=(xyz.x,10.5,xyz.z);bore=cyl(2.1,5,*point)
                assert abs(bore.intersect(fit[receiver]).Volume()-bore.Volume())<.05,(receiver,point)
                fit[receiver]=fit[receiver].cut(bore).clean()
                new_inserts.append({'part':receiver,'entry':list(point),'axis':[0,1,0],'depth':5,'length':4})
            else:
                inside=plane.toWorldCoords(V(uu,vv,0 if sign==1 else 10))
                # Conservative washer/nut cylinder, inside the sheet.
                nut_envelopes[f'nut_{len(nut_envelopes)+1:02d}']=cyl(3.5,3,*inside.toTuple(),axis.toTuple())
            extra.append({'label':'prototype_splice','start':list(start.toTuple()),'axis':list(axis.toTuple()),'length':20,'receiver':receiver})
        splices[name]=place(s.clean(),p)
    # Fewest rectangular subdivisions for these outlines under the A1 envelope.
    # Unequal front/rear rows keep critical holes and the brace away from seams.
    cuts={
        'front':([0,110,220],[0,125,270,380]),'rear':([0,110,220],[0,125,280,380]),
        'left':([0,ps['left']['size'][0]/2,ps['left']['size'][0]],[0,179.5,359]),
        'right':([0,ps['right']['size'][0]/2,ps['right']['size'][0]],[0,179.5,359])}
    for n in ['top','bottom','brace']:
        a,b=ps[n]['size'];cuts[n]=([0,a/2,a],[0,b/2,b])
    for u in [14,206]:
        for v in [125,270]:splice('front',u,v,'strip','v')
    splice('front',110,35,'strip')
    for v in [125,280]:splice('rear',110,v,'cross')
    for n in ['left','right','top','bottom']:
        a,b=ps[n]['size'];splice(n,a/2,b/2,'cross')
    a,b=ps['brace']['size']
    for v in [18,b-18]:splice('brace',a/2,v,'strip')
    for u in [15,a-15]:splice('brace',u,b/2,'strip','v')
    for n,p in ps.items():
        xs,ys=cuts[n];full=panel_shape(p)
        for ix in range(len(xs)-1):
            for iy in range(len(ys)-1):
                u=xs[ix]+(.25 if ix else 0);v=ys[iy]+(.25 if iy else 0)
                du=xs[ix+1]-(.25 if ix<len(xs)-2 else 0)-u;dv=ys[iy+1]-(.25 if iy<len(ys)-2 else 0)-v
                s=full.intersect(box(u,v,-1,du,dv,12)).translate((-u,-v,0)).clean()
                assert s.isValid() and len(s.Solids())==1,(n,ix,iy)
                name=f'{n}_{ix+1}{iy+1}';tile_info[name]={'parent':n,'offset':[u,v],'size':[du,dv]}
                tiles[name]=(s,place(s.translate((u,v,0)),p))
    # Restore removed brace material / receiver drillings, then deduct new parts.
    removed=fullpanels['brace']
    for n,(_,s) in tiles.items():
        if n.startswith('brace_'):removed=removed.cut(s)
    air=air.fuse(removed).clean()
    for n in fit:
        if n.startswith('rail_'):air=air.fuse(original[n].cut(fit[n])).clean()
    for n,s in splices.items():
        if '_brace_' in n:air=air.cut(s).clean()
    D=meta['dimensions_mm'][1]
    air=air.cut(box(-10,D-45,290,10,10,40)).clean()
    return ps,tiles,fit,splices,air,{'tile_info':tile_info,'extra_bolts':extra,'extra_inserts':new_inserts,
        'nut_envelopes':nut_envelopes,'prototype_hardware_allowance_litres':.004,
        'nominal_net_litres':air.Volume()/1e6,'cuts':cuts}

def svg_from_dxf(path,width,height):
    doc=ezdxf.readfile(path);elements=[]
    def num(x):return f'{x:.8f}'
    for e in doc.modelspace():
        kind=e.dxftype()
        if kind=='LINE':
            a,b=e.dxf.start,e.dxf.end;elements.append(f'<path d="M {num(a.x)} {num(a.y)} L {num(b.x)} {num(b.y)}"/>')
        elif kind=='CIRCLE':
            c=e.ocs().to_wcs(e.dxf.center);elements.append(f'<circle cx="{num(c.x)}" cy="{num(c.y)}" r="{num(e.dxf.radius)}"/>')
        elif kind=='ARC':
            a,b=list(e.vertices([e.dxf.start_angle,e.dxf.end_angle]));r=e.dxf.radius
            large=int((e.dxf.end_angle-e.dxf.start_angle)%360>180);sweep=int(e.dxf.extrusion.z>0)
            elements.append(f'<path d="M {num(a.x)} {num(a.y)} A {num(r)} {num(r)} 0 {large} {sweep} {num(b.x)} {num(b.y)}"/>')
        else:raise ValueError('Unexpected 2D entity '+kind)
    path.with_suffix('.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.8f}mm" height="{height:.8f}mm" viewBox="0 0 {width:.8f} {height:.8f}"><g transform="translate(0 {height:.8f}) scale(1 -1)" fill="none" stroke="black" stroke-width="0.1">'+''.join(elements)+'</g></svg>\n')

def sheet_export(shape,folder,name,size):
    face=min(shape.Faces(),key=lambda f:f.Center().z)
    path=folder/'laser'/f'{name}.dxf'
    cq.exporters.exportDXF(cq.Workplane('XY').add(face),str(path))
    svg_from_dxf(path,*size)
    rebuilt=cq.importers.importDXF(str(path)).wires().toPending().extrude(10).val()
    error=shape.cut(rebuilt).Volume()+rebuilt.cut(shape).Volume()
    assert error<.05,(name,'DXF mismatch',error)
    return {'part':name,'DXF_symmetric_difference_mm3':error,'SVG_source':'same DXF entities','thickness_mm':10}

def orient_fitting(name,s):
    if name.startswith('rail_'):
        return s.rotate((0,0,0),(0,1,0),-90 if '_left_' in name else 90).rotate((0,0,0),(0,0,1),45)
    return s.rotate((0,0,0),(1,0,0),-90)

def mesh_export(shape,path,require_fit=True):
    assert shape.isValid() and len(shape.Solids())==1,path.name
    bb=shape.BoundingBox();s=shape.translate((-bb.xmin,-bb.ymin,-bb.zmin))
    cq.exporters.export(s,str(path),tolerance=.02,angularTolerance=.08)
    m=trimesh.load_mesh(path);m.apply_translation(-m.bounds[0]);m.export(path);m=trimesh.load_mesh(path)
    fit=bool((m.extents<=[178.0001,178.0001,180.0001]).all())
    good=bool(m.is_watertight and m.is_winding_consistent and m.volume>0 and len(m.split())==1)
    assert good and (fit or not require_fit),(path.name,m.extents,good)
    return {'file':path.name,'size_mm':m.extents.tolist(),'solid_cm3':shape.Volume()/1000,'manifold':good,'fits_A1':fit,'quantity':1}

def export_all(data):
    panels,fullpanels,fittings,proxies,air,meta=data
    ps,tiles,protofit,splices,protoair,pm=prototype(data)
    # Replace obsolete manufacturing outputs; synced references are untouched.
    for old in ['stl','step','exports']:
        folder=ROOT/old
        if folder.exists():shutil.rmtree(folder)
    records={};profiles=[]
    for variant in ['unrestricted','a1_mini']:
        folder=ROOT/'exports'/variant
        for sub in ['laser','stl','step']:(folder/sub).mkdir(parents=True,exist_ok=True)
        rows=[];assembly={}
        for n,p in (panels.items() if variant=='unrestricted' else tiles.items()):
            if variant=='unrestricted':localshape=panel_shape(p);globalshape=fullpanels[n];size=p['size']
            else:localshape,globalshape=p;size=pm['tile_info'][n]['size']
            profiles.append({'variant':variant,**sheet_export(localshape,folder,n,size)})
            oriented=localshape;orientation='flat'
            if variant=='a1_mini' and size[1]>178:
                oriented=localshape.rotate((0,0,0),(1,0,0),90);orientation='upright, 10 mm edge on bed'
            row=mesh_export(oriented,folder/'stl'/f'{n}.stl',variant=='a1_mini')
            row.update({'kind':'sheet','orientation':orientation});rows.append(row);assembly[n]=globalshape
        fits=fittings if variant=='unrestricted' else protofit
        for n,s in fits.items():
            row=mesh_export(orient_fitting(n,s),folder/'stl'/f'{n}.stl');row.update({'kind':'printed_fitting','orientation':'supplied'});rows.append(row);assembly[n]=s
        if variant=='a1_mini':
            assembly.update(splices)
            for kind,dx,dy,centres in [('strip',28,16,[(-8,0),(8,0)]),('cross',28,28,[(-8,-8),(-8,8),(8,-8),(8,8)])]:
                s=box(-dx/2,-dy/2,0,dx,dy,4)
                for x,y in centres:s=s.cut(cyl(1.7,6,x,y,-1,(0,0,1)))
                row=mesh_export(s,folder/'stl'/f'splice_{kind}.stl');row.update({'kind':'prototype_only','orientation':'flat','quantity':sum(n.endswith(kind) for n in splices)});rows.append(row)
        for n,s in assembly.items():cq.exporters.export(s,str(folder/'step'/f'{n}.step'))
        cq.exporters.export(compound(assembly.values()),str(folder/'step/enclosure_assembly.step'))
        cq.exporters.export(compound([*assembly.values(),*proxies.values()]),str(folder/'step/assembly_with_components.step'))
        cq.exporters.export(air if variant=='unrestricted' else protoair,str(folder/'step/nominal_air_volume.step'))
        for n,s in proxies.items():cq.exporters.export(s,str(folder/'step'/f'reference_{n}.step'))
        records[variant]={'parts':rows,'assembly_parts':list(assembly),'physical_piece_count':sum(r['quantity'] for r in rows),
            'sheet_pieces':7 if variant=='unrestricted' else len(tiles),'nominal_net_litres':meta['volume']['nominal_net_litres'] if variant=='unrestricted' else pm['nominal_net_litres']}
        with (folder/'print-manifest.csv').open('w') as f:
            w=csv.writer(f);w.writerow(['file','quantity','kind','size_x_mm','size_y_mm','size_z_mm','orientation','fits_A1'])
            for r in rows:w.writerow([r['file'],r['quantity'],r['kind'],*r['size_mm'],r['orientation'],r['fits_A1']])
    coupon={'size':[80,50],'rect_cuts':[[10,27,10,15],[35,27,10.2,15],[60,27,10.4,15]],'holes':[{'u':x,'v':12,'diameter':d} for x,d in [(15,4.5),(35,4.7),(55,5)]]}
    folder=ROOT/'exports/calibration';(folder/'laser').mkdir(parents=True);(folder/'stl').mkdir()
    s=panel_shape(coupon);sheet_export(s,folder,'sheet_fit_coupon',[80,50]);mesh_export(s,folder/'stl/sheet_fit_coupon.stl')
    meta['variants']=records;meta['panel_profiles']=panels;meta['prototype_profiles']=ps;meta['prototype_tiles']=pm['tile_info'];meta['prototype_cuts']=pm['cuts']
    meta['prototype_bolts']=pm['extra_bolts'];meta['prototype_inserts']=pm['extra_inserts'];meta['profile_checks']=profiles
    meta['prototype_hardware_allowance_litres']=.004
    (ROOT/'validation/geometry_report.json').write_text(json.dumps(meta,indent=2))
    (ROOT/'validation/prototype_nuts.json').write_text(json.dumps(list(pm['nut_envelopes']),indent=2))
    for n,s in pm['nut_envelopes'].items():cq.exporters.export(s,str(ROOT/'exports/a1_mini/step'/f'reference_{n}.step'))
    print(json.dumps({'dimensions_mm':meta['dimensions_mm'],'variants':{n:{k:v for k,v in r.items() if k not in ['parts','assembly_parts']} for n,r in records.items()}},indent=2))
