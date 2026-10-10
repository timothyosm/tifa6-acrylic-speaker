"""Collect the current whole-panel / single-port build without changing its geometry."""
from speaker_assembly import *
import csv, shutil
import trimesh
base=ROOT/'exports';dest=base/'current'
for sub in ['stl','laser','step']:(dest/sub).mkdir(parents=True,exist_ok=True)
m=json.loads((ROOT/'validation/geometry_report.json').read_text());D=m['dimensions_mm'][1]
names=list(m['variants']['unrestricted']['assembly_parts'])
names=[n for n in names if n not in ['port_inlet','port_mouth']]+['bass_reflex_port']
assert len(names)==19
rows=[];parts={}
for n in names:
    source=base/'one_piece_port' if n=='bass_reflex_port' else base/'unrestricted/stl'
    shutil.copy2(source/(n+'.stl'),dest/'stl'/(n+'.stl'))
    mesh=trimesh.load_mesh(dest/'stl'/(n+'.stl'))
    assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1 and mesh.volume>0
    rows.append({'file':n+'.stl','quantity':1,'kind':'sheet' if n in m['panel_profiles'] else 'fitting','size_mm':mesh.extents.tolist(),'watertight':True})
    if n=='bass_reflex_port':
        printed=cq.importers.importStep(str(base/'one_piece_port/bass_reflex_port.step')).val()
        s=printed.translate((-48,-48,0)).rotate((0,0,0),(1,0,0),90).translate((0,D+3.5,55))
    else:s=cq.importers.importStep(str(base/'unrestricted/step'/(n+'.step'))).val()
    assert s.isValid() and len(s.Solids())==1
    parts[n]=s;cq.exporters.export(s,str(dest/'step'/(n+'.step')))
for n in m['panel_profiles']:
    for ext in ['dxf','svg']:shutil.copy2(base/'unrestricted/laser'/(n+'.'+ext),dest/'laser'/(n+'.'+ext))
refs={}
for n in ['woofer','tweeter','crossover','spacers']:
    refs[n]=cq.importers.importStep(str(base/'unrestricted/step'/('reference_'+n+'.step'))).val()
    cq.exporters.export(refs[n],str(dest/'step'/('reference_'+n+'.step')))
port=parts['bass_reflex_port'];collisions=[]
for n,s in {**parts,**refs}.items():
    if n!='bass_reflex_port' and port.intersect(s).Volume()>.05:collisions.append(n)
assert not collisions,collisions
cq.exporters.export(compound(parts.values()),str(dest/'step/enclosure_assembly.step'))
cq.exporters.export(compound([*parts.values(),*refs.values()]),str(dest/'step/assembly_with_components.step'))
# The old air solid excluded the entire coupling collar envelope. Restore the
# annulus removed by the continuous 54 mm OD duct. Hardware allowance stays fixed.
air=cq.importers.importStep(str(base/'unrestricted/step/nominal_air_volume.step')).val()
j=m['port_joint_y'];restore=cyl(36,8.5,0,j-4.25,55).cut(cyl(27,8.5,0,j-4.25,55))
for s in [*parts.values(),*refs.values()]:restore=restore.cut(s)
air=air.fuse(restore).clean();assert air.isValid()
cq.exporters.export(air,str(dest/'step/nominal_air_volume.step'))
report={'all_pass':True,'variant':'whole panels and one-piece port','dimensions_width_depth_height_mm':m['dimensions_mm'],'STL_count':19,'sheet_parts':7,'printed_fittings':12,'physical_piece_count':19,'nominal_net_litres':air.Volume()/1e6,'M3_screws':72,'M3_inserts':60,'M3_plain_nuts':4,'port_component_interferences':collisions,'parts':rows,'physical_testing_performed':False,'scope':'Current meshes rechecked; unchanged panel/fitting checks inherited from interference_report.json. New port checked against saved assembly and component envelopes. Volume includes unchanged estimated hardware and component allowances.'}
(dest/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'validation/current_build_report.json').write_text(json.dumps(report,indent=2)+'\n')
with (dest/'print-manifest.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['file','quantity','kind','size_x_mm','size_y_mm','size_z_mm'])
    for r in rows:w.writerow([r['file'],1,r['kind'],*r['size_mm']])
with (dest/'fastener-map.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['purpose','length_mm','head_x','head_y','head_z','axis_x','axis_y','axis_z','receiver'])
    for b in m['bolts']:
        if b['label']!='port_coupling_nut':w.writerow([b['label'],b['length'],*b['start'],*b['axis'],b['receiver'] or 'nut_or_spacer'])
print(json.dumps({k:v for k,v in report.items() if k!='parts'},indent=2))
