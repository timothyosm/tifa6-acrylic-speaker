"""Check saved SVG geometry against DXF entities, independently of export code."""
from pathlib import Path
import json, math, re
import xml.etree.ElementTree as ET
import ezdxf, trimesh
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'validation/geometry_report.json').read_text());records=[]
def close(a,b):return abs(a-b)<1e-6
for rec in m['profile_checks']:
 name=rec['part'];variant=rec['variant'];base=ROOT/'exports'/variant
 size=m['panel_profiles'][name]['size']
 root=ET.parse(base/'laser'/(name+'.svg')).getroot();g=list(root)[0]
 assert close(float(root.attrib['width'][:-2]),size[0]) and close(float(root.attrib['height'][:-2]),size[1])
 assert g.attrib['transform']==f'translate(0 {size[1]:.8f}) scale(1 -1)'
 entities=list(ezdxf.readfile(base/'laser'/(name+'.dxf')).modelspace())
 assert len(entities)==len(g)
 for e,el in zip(entities,list(g)):
  kind=e.dxftype()
  if kind=='CIRCLE':
   c=e.ocs().to_wcs(e.dxf.center)
   assert el.tag.endswith('circle') and all(close(float(el.attrib[k]),v) for k,v in [('cx',c.x),('cy',c.y),('r',e.dxf.radius)])
  else:
   nums=list(map(float,re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?',el.attrib['d'])))
   if kind=='LINE':
    a,b=e.dxf.start,e.dxf.end;expected=[a.x,a.y,b.x,b.y]
   else:
    assert kind=='ARC'
    a,b=list(e.vertices([e.dxf.start_angle,e.dxf.end_angle]));delta=(e.dxf.end_angle-e.dxf.start_angle)%360
    expected=[a.x,a.y,e.dxf.radius,e.dxf.radius,0,int(delta>180),int(e.dxf.extrusion.z>0),b.x,b.y]
   assert len(nums)==len(expected) and all(close(a,b) for a,b in zip(nums,expected)),name
 mesh=trimesh.load_mesh(base/'stl'/(name+'.stl'))
 assert min(abs(float(x)-10) for x in mesh.extents)<1e-4
 records.append({'variant':variant,'part':name,'SVG_geometry_matches_DXF':True,'STL_thickness_10_mm':True})
result={'all_pass':True,'profiles':records,'scope':'SVG circle/line/arc coordinates, direction, units and viewport compared to saved DXF; sheet mesh thickness checked. DXF-to-CAD roundtrip is in geometry_report.json.'}
(ROOT/'validation/profile_report.json').write_text(json.dumps(result,indent=2));print('Verified',len(records),'matching profiles and sheet thicknesses')
