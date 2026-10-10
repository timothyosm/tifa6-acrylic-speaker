"""Whole bass-reflex port for an unrestricted printer; existing rear-panel fit."""
from speaker_assembly import *
import trimesh
folder=ROOT/'exports/one_piece_port';folder.mkdir(parents=True,exist_ok=True)
m=json.loads((ROOT/'validation/geometry_report.json').read_text());D=m['dimensions_mm'][1]
r=25;L=185;R=14
outer=(cq.Workplane('XZ').moveTo(0,-L).lineTo(0,0).lineTo(48,0).lineTo(48,-3)
       .lineTo(36.25,-3).lineTo(36.25,-14).lineTo(27,-30).lineTo(27,-L).close().revolve(360,(0,0),(0,1)).val())
inner=(cq.Workplane('XZ').moveTo(0,-L-1).lineTo(r,-L-1).lineTo(r,-R)
       .threePointArc((r+R-R/math.sqrt(2),-R+R/math.sqrt(2)),(r+R,0))
       .lineTo(r+R,1).lineTo(0,1).close().revolve(360,(0,0),(0,1)).val())
port=outer.cut(inner)
for a in [45,135,225,315]:
    x=44*math.cos(math.radians(a));y=44*math.sin(math.radians(a))
    port=port.cut(cyl(1.7,5,x,y,-4,(0,0,1)))
port=port.clean();assert port.isValid() and len(port.Solids())==1
printed=port.rotate((0,0,0),(1,0,0),180).translate((48,48,0))
cq.exporters.export(printed,str(folder/'bass_reflex_port.stl'),tolerance=.01,angularTolerance=.05)
cq.exporters.export(printed,str(folder/'bass_reflex_port.step'))
mesh=trimesh.load_mesh(folder/'bass_reflex_port.stl')
assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1 and mesh.volume>0
assert all(abs(a-b)<.0001 for a,b in zip(mesh.extents,[96,96,185]))
global_port=port.rotate((0,0,0),(1,0,0),-90).translate((0,D+3.5,55))
conflicts=[]
for name in m['variants']['unrestricted']['assembly_parts']:
    if name in ['port_inlet','port_mouth']:continue
    s=cq.importers.importStep(str(ROOT/'exports/unrestricted/step'/(name+'.step'))).val()
    if global_port.intersect(s).Volume()>.03:conflicts.append(name)
assert not conflicts,conflicts
old=sum(cq.importers.importStep(str(ROOT/'exports/unrestricted/step'/(n+'.step'))).val().Volume() for n in ['port_inlet','port_mouth'])
report={'all_pass':True,'size_mm':mesh.extents.tolist(),'bore_mm':50,'axial_length_mm':185,'outlet_flare_radius_mm':14,'flange_diameter_mm':96,'spigot_diameter_mm':72.5,'rear_panel_opening_mm':73,'M3_clearance_holes':4,'hole_diameter_mm':3.4,'hole_PCD_mm':88,'watertight':True,'single_solid':True,'assembly_interferences':conflicts,'approx_net_volume_gain_litres':(old-port.Volume())/1e6,'physical_print_tested':False}
(folder/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
(folder/'PRINT-NOTES.txt').write_text('ONE-PIECE BASS-REFLEX PORT\n\nPrint one bass_reflex_port.stl at 100% scale, millimetres.\n50 mm bore, 185 mm mouth-to-inlet length, R14 outlet flare.\n96 mm flange with four M3 clearance holes on 88 mm PCD.\nMatches the existing 73 mm rear-panel hole.\n\nThe flange is already flat on the bed. Preview local supports at the\nflared mouth; keep the long vertical bore clear of unnecessary supports.\nRemove supports and inspect the bore before assembly.\n\nUse the existing 0.5 mm compressed flange gasket and four M3 x20\nbolts with washers and rear nuts. No port coupling gasket or coupling\nbolts are needed: this replaces BOTH older printed port halves.\nThe obsolete middle coupling collar has been removed. Geometry and\nassembly clearance checks pass; physical printing is not yet tested.\n')
print(json.dumps(report,indent=2))
