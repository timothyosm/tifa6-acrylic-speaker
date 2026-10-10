"""Whole laser panels, matching flat STLs, and acrylic-enclosure fittings."""
from speaker_assembly import *
import csv
import trimesh, ezdxf

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

def mesh_export(shape,path):
    assert shape.isValid() and len(shape.Solids())==1,path.name
    bb=shape.BoundingBox();s=shape.translate((-bb.xmin,-bb.ymin,-bb.zmin))
    cq.exporters.export(s,str(path),tolerance=.02,angularTolerance=.08)
    mesh=trimesh.load_mesh(path);mesh.apply_translation(-mesh.bounds[0]);mesh.export(path)
    good=bool(mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0 and len(mesh.split())==1)
    assert good,path.name
    return {'file':path.name,'size_mm':mesh.extents.tolist(),'solid_cm3':shape.Volume()/1000,'manifold':good,'quantity':1}

def export_all(data):
    panels,fullpanels,fittings,proxies,air,meta=data
    folder=ROOT/'exports/current'
    for sub in ['laser','stl','step']:(folder/sub).mkdir(parents=True,exist_ok=True)
    rows=[];profiles=[];assembly={**fullpanels,**fittings}
    for n,p in panels.items():
        shape=panel_shape(p)
        profiles.append({'variant':'current',**sheet_export(shape,folder,n,p['size'])})
        row=mesh_export(shape,folder/'stl'/(n+'.stl'));row.update({'kind':'sheet','orientation':'flat'});rows.append(row)
    for n,s in fittings.items():
        row=mesh_export(orient_fitting(n,s),folder/'stl'/(n+'.stl'));row.update({'kind':'printed_fitting','orientation':'supplied'});rows.append(row)
    for n,s in assembly.items():cq.exporters.export(s,str(folder/'step'/(n+'.step')))
    cq.exporters.export(compound(assembly.values()),str(folder/'step/enclosure_assembly.step'))
    cq.exporters.export(compound([*assembly.values(),*proxies.values()]),str(folder/'step/assembly_with_components.step'))
    cq.exporters.export(air,str(folder/'step/nominal_air_volume.step'))
    for n,s in proxies.items():cq.exporters.export(s,str(folder/'step'/('reference_'+n+'.step')))
    info={'parts':rows,'assembly_parts':list(assembly),'physical_piece_count':len(assembly),'sheet_pieces':7,'nominal_net_litres':air.Volume()/1e6}
    meta.update({'variants':{'current':info},'panel_profiles':panels,'profile_checks':profiles})
    (ROOT/'validation/geometry_report.json').write_text(json.dumps(meta,indent=2)+'\n')
    with (folder/'print-manifest.csv').open('w') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['file','quantity','kind','size_x_mm','size_y_mm','size_z_mm'])
        for row in rows:w.writerow([row['file'],1,row['kind'],*row['size_mm']])
    with (folder/'fastener-map.csv').open('w') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['purpose','length_mm','head_x','head_y','head_z','axis_x','axis_y','axis_z','receiver'])
        for b in meta['bolts']:w.writerow([b['label'],b['length'],*b['start'],*b['axis'],b['receiver'] or 'nut_or_spacer'])
    coupon={'size':[80,50],'rect_cuts':[[10,27,10,15],[35,27,10.2,15],[60,27,10.4,15]],'holes':[{'u':x,'v':12,'diameter':d} for x,d in [(15,4.5),(35,4.7),(55,5)]]}
    calibration=ROOT/'exports/calibration'
    for sub in ['laser','stl']:(calibration/sub).mkdir(parents=True,exist_ok=True)
    shape=panel_shape(coupon);sheet_export(shape,calibration,'sheet_fit_coupon',[80,50]);mesh_export(shape,calibration/'stl/sheet_fit_coupon.stl')
    print(json.dumps({'parts':len(assembly),'panels':7,'fittings':len(fittings),'nominal_net_litres':air.Volume()/1e6},indent=2))
