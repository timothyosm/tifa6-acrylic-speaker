"""Export only whole 10 mm laser-profile panels for an unrestricted test printer."""
from pathlib import Path
import csv, json, shutil, zipfile, hashlib
import cadquery as cq
import trimesh
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
meta=json.loads((ROOT/'validation/geometry_report.json').read_text())
source=ROOT/'exports/unrestricted';target=ROOT/'exports/whole_panels'
target.mkdir(parents=True,exist_ok=True);(target/'laser_profiles').mkdir(exist_ok=True)
records=[]
for name in ['front','rear','left','right','top','bottom','brace']:
    # Reuse the checked whole-panel meshes; no rescaling or prototype modifications.
    dest=target/(name+'.stl');shutil.copy2(source/'stl'/(name+'.stl'),dest)
    mesh=trimesh.load_mesh(dest)
    size=meta['panel_profiles'][name]['size']+[10]
    assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1 and mesh.volume>0
    assert all(abs(float(a)-b)<.0001 for a,b in zip(mesh.extents,size))
    assert abs(float(mesh.bounds[0,2]))<.0001
    # Re-extrude the saved cutting profile and compare its volume to the saved mesh.
    solid=cq.importers.importDXF(str(source/'laser'/(name+'.dxf'))).wires().toPending().extrude(10).val()
    err=abs(mesh.volume-solid.Volume())/solid.Volume()
    assert solid.isValid() and len(solid.Solids())==1 and err<.0002,(name,err)
    for ext in ['dxf','svg']:shutil.copy2(source/'laser'/(name+'.'+ext),target/'laser_profiles'/(name+'.'+ext))
    records.append({'part':name,'quantity':1,'size_mm':[float(v) for v in mesh.extents],
        'watertight':True,'single_connected_mesh':True,'flat_on_bed':True,'mesh_vs_DXF_extrusion_relative_volume_error':float(err)})
readme='''WHOLE LASER-PANEL TEST PRINTS

Print ONE of each of the seven STL files: front, rear, left, right,
top, bottom and brace. These are six outer panels plus the internal brace.

All are flat, full-size, 10 mm-thick panels in millimetres, already lying
on the print bed. No printer-size limit, scaling, tile seams, splice strips
or extra prototype holes are applied. Use 100% scale in the slicer.

The laser_profiles folder contains the matching DXF and SVG outlines.
Use ONE format for laser cutting, not both. Profiles have no kerf compensation.
Confirm actual stock thickness and laser kerf before cutting acrylic.

Cabinet dimensions: 220 mm wide x 380 mm high x 262.652160 mm deep.
Panel dimensions and quantities are in panel-list.csv.

This download contains only the requested sheet-shaped parts. The M3 holes,
circular adapter openings and brace clearances match the existing acrylic
CAD design. Driver adapters, corner fittings and the port are not flat laser
panels, so are not included in this panel-only download. They remain in the
existing project if needed for an assembled fit test. No aluminium-rail or
solvent-bonding redesign was applied.

STL represents a solid, so '2D STL' here means an exact panel outline
extruded to the intended acrylic thickness. SVG/DXF are the true 2D files.
'''
(target/'START-HERE.txt').write_text(readme)
with (target/'panel-list.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['part','quantity','width_mm','height_mm','thickness_mm'])
    for r in records:w.writerow([r['part'],1,*r['size_mm']])
report={'all_pass':True,'scope':'Whole panels only. No printer-size constraint. Same profiles as unrestricted acrylic set.','parts':records}
(target/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'validation/whole_panel_report.json').write_text(json.dumps(report,indent=2)+'\n')
# Overview from the actual SVG cutting paths, with panel labels and dimensions.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="950" viewBox="0 0 1440 950">',
 '<rect width="1440" height="950" fill="#f4f5f6"/>',
 '<g font-family="Helvetica,Arial,sans-serif" fill="#20252b"><text x="38" y="43" font-size="27">Whole acrylic panels / flat STL test set</text><text x="38" y="73" font-size="17">7 pieces · 10 mm thick · full size · no printer splits</text></g>']
for i,r in enumerate(records):
    n=r['part'];w,h=r['size_mm'][:2];x=38+(i%4)*354;y=115+(i//4)*410;scale=min(300/w,340/h)
    original=ET.parse(target/'laser_profiles'/(n+'.svg')).getroot();group=list(original)[0]
    group.set('stroke-width','0.85');group.set('stroke','#2f6374')
    svg.append(f'<g transform="translate({x} {y})"><text font-family="Helvetica,Arial,sans-serif" font-size="17" fill="#20252b">{n.upper()}  /  {w:.2f} × {h:.2f}</text><g transform="translate(0 18) scale({scale})">{ET.tostring(group,encoding="unicode")}</g></g>')
svg.append('</svg>');(target/'panel-overview.svg').write_text(''.join(svg))
archive=ROOT.parent/'tifa-whole-panel-stls.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(target.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(target))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps({'archive':str(archive),'STL_files':7,'parts':records},indent=2))
