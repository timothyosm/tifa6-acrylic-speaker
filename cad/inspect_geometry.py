"""Independent checks of saved STEP, STL and laser-profile round trips."""
from speaker_assembly import *
from itertools import combinations
from OCP.BRepAdaptor import BRepAdaptor_Surface
import trimesh, ezdxf, xml.etree.ElementTree as ET
m=json.loads((ROOT/'validation/geometry_report.json').read_text());checks={};issues={}

def overlap(a,b):
    aa=a.BoundingBox();bb=b.BoundingBox()
    if any(getattr(aa,k+'max')<getattr(bb,k+'min')+1e-6 or getattr(bb,k+'max')<getattr(aa,k+'min')+1e-6 for k in 'xyz'):return 0
    return a.intersect(b).Volume()
def load(folder,n):return cq.importers.importStep(str(folder/(n+'.step'))).val()

def edge_clearance(p):
    s=panel_shape(p);bottom=min(s.Faces(),key=lambda f:f.Center().z);result=[]
    for h in p['holes']:
        if h['diameter']!=4.5:continue
        pt=cq.Vertex.makeVertex(h['u'],h['v'],0);ds=[]
        for e in bottom.Edges():
            if e.geomType()=='CIRCLE':
                c=e.arcCenter()
                if math.hypot(c.x-h['u'],c.y-h['v'])<1e-4:continue
            ds.append(pt.distance(e))
        if ds:result.append(min(ds))
    return result

for variant,info in m['variants'].items():
    print('Inspecting',variant,flush=True)
    base=ROOT/'exports'/variant;folder=base/'step'
    parts={n:load(folder,n) for n in info['assembly_parts']}
    proxies={n:load(folder,'reference_'+n) for n in ['woofer','tweeter','crossover','spacers']}
    bad=[]
    for (an,a),(bn,b) in combinations(parts.items(),2):
        v=overlap(a,b)
        if v>.05:bad.append([an,bn,v])
    checks[variant+'_no_part_interference']=not bad;issues[variant+'_part_interference']=bad
    bad=[]
    for n,p in proxies.items():
        for nn,s in parts.items():
            v=overlap(p,s)
            if v>.05:bad.append([n,nn,v])
    checks[variant+'_component_clearance']=not bad;issues[variant+'_component_interference']=bad
    bolts=m['bolts']+(m['prototype_bolts'] if variant=='a1_mini' else [])
    bad=[];heads=[];washers=[]
    for i,b in enumerate(bolts):
        shaft=cyl(1.45,b['length'],*b['start'],b['axis'])
        a=V(*b['axis']);p=V(*b['start'])-a.multiply(3)
        head=cyl(2.75,3,*p.toTuple(),b['axis'])
        radius=3.5 if b['label']=='port_coupling_nut' else 4.5
        washer=cyl(radius,1.5,*b['start'],b['axis']).cut(cyl(1.7,1.5,*b['start'],b['axis']))
        for n,s in parts.items():
            v=overlap(shaft,s)
            if v>.03:bad.append([i,b['label'],n,v])
            v=overlap(head,s)
            if v>.05:heads.append([i,n,v])
            if b['label'] not in ['woofer_driver','tweeter_driver','crossover_board']:
                v=overlap(washer,s)
                if v>.05:washers.append([i,n,v])
    checks[variant+'_all_screw_shafts_clear']=not bad;issues[variant+'_shaft_interference']=bad
    checks[variant+'_screw_heads_clear']=not heads;issues[variant+'_head_interference']=heads
    checks[variant+'_washers_clear']=not washers;issues[variant+'_washer_interference']=washers
    ins=m['inserts']+(m['prototype_inserts'] if variant=='a1_mini' else [])
    bores=[];engagement=[]
    for rec in ins:
        s=parts[rec['part']];probe=cyl(2.0,rec['length'],*rec['entry'],rec['axis'])
        if overlap(probe,s)>.01:bores.append(rec)
    for b in bolts:
        if b['receiver']:
            candidates=[r for r in ins if r['part']==b['receiver'] and abs(V(*r['axis']).dot(V(*b['axis']))-1)<1e-6 and (V(*r['entry'])-V(*b['start'])).cross(V(*b['axis'])).Length<1e-4]
            if len(candidates)!=1:engagement.append([b,'missing/ambiguous receiver']);continue
            r=candidates[0];dist=(V(*r['entry'])-V(*b['start'])).dot(V(*b['axis']));penetration=b['length']-dist
            if penetration<3.5-1e-6 or penetration>r['depth']-.4+1e-6:engagement.append([b,penetration,r['depth']])
    checks[variant+'_insert_bores_clear']=not bores;checks[variant+'_thread_engagement_and_bottom_clearance']=not engagement
    issues[variant+'_insert_issues']=bores;issues[variant+'_engagement_issues']=engagement
    allfits=[];stlbad=[]
    for row in info['parts']:
        s=trimesh.load_mesh(base/'stl'/row['file']);valid=bool(s.is_watertight and s.is_winding_consistent and s.volume>0 and len(s.split())==1)
        fit=bool((s.extents<=[178.0001,178.0001,180.0001]).all())
        if not valid or abs(s.bounds[0,2])>1e-5:stlbad.append(row['file'])
        if variant=='a1_mini' or row['kind']!='sheet':allfits.append(fit)
    checks[variant+'_manifold_STLs']=not stlbad;checks[variant+'_required_parts_fit_A1']=all(allfits)
    checks[variant+'_valid_single_CAD_solids']=all(s.isValid() and len(s.Solids())==1 for s in parts.values())
    air=load(folder,'nominal_air_volume')
    checks[variant+'_saved_air_volume_matches']=air.isValid() and abs(air.Volume()/1e6-info['nominal_net_litres'])<1e-6
    D=m['dimensions_mm'][1];mouth=m['port_mouth_y'];pz=P['port_centre_z']
    approach=cyl(25,50,0,mouth-235,pz)
    checks[variant+'_port_inlet_one_diameter_clear']=all(overlap(approach,s)<.03 for s in [*parts.values(),*proxies.values()])
    gauge=cyl(24.99,171,0,mouth-185,pz)
    checks[variant+'_port_50_mm_bore_clear']=all(overlap(gauge,s)<.03 for s in parts.values())
    port=compound([parts['port_inlet'],parts['port_mouth']])
    checks[variant+'_port_185_mm_length']=abs(port.BoundingBox().ylen-185)<.001
    woofer_envelope=cq.Solid.makeCone(72.25,42.5,76.7,V(0,3.6,160),V(0,1,0))
    checks[variant+'_woofer_conservative_envelope_clear']=all(overlap(woofer_envelope,s)<.05 for s in parts.values())
    if variant=='a1_mini':
        bad=[]
        for path in folder.glob('reference_nut_*.step'):
            nut=cq.importers.importStep(str(path)).val()
            for n,s in {**parts,**proxies}.items():
                v=overlap(nut,s)
                if v>.05:bad.append([path.stem,n,v])
        checks['prototype_nuts_and_washers_clear']=not bad;issues['prototype_nut_interferences']=bad
# Exact nominal profile match, including SVG scale and entity counts.
checks['all_DXF_roundtrips_match_STL_source']=all(r['DXF_symmetric_difference_mm3']<.05 for r in m['profile_checks'])
svg_bad=[]
for r in m['profile_checks']:
    path=ROOT/'exports'/r['variant']/'laser'/(r['part']+'.svg');root=ET.parse(path).getroot()
    ents=list(ezdxf.readfile(path.with_suffix('.dxf')).modelspace());elements=list(list(root)[0])
    if len(ents)!=len(elements) or not root.attrib['width'].endswith('mm') or not root.attrib['height'].endswith('mm'):svg_bad.append(str(path))
checks['SVG_units_and_entity_counts_match_DXF']=not svg_bad
clearances={n:min(edge_clearance(p)) for n,p in m['panel_profiles'].items()}
checks['acrylic_M3_hole_centres_at_least_6_75_mm_from_edges']=min(clearances.values())>=6.75-1e-5
# Independent nominal rectangular tiling lower bound (flat or upright, no tilted supports).
minimum={}
for n,p in m['panel_profiles'].items():
    a,b=p['size'];minimum[n]=min(i*j for i in range(1,8) for j in range(1,8) if (a/i<=178 and b/j<=180) or (a/i<=180 and b/j<=178))
checks['minimum_regular_rectangular_tile_counts']=all(sum(t['parent']==n for t in m['prototype_tiles'].values())==cnt for n,cnt in minimum.items())
checks['production_net_target_16_1_litres']=abs(m['variants']['unrestricted']['nominal_net_litres']-16.1)<1e-5
result={'all_pass':all(checks.values()),'checks':checks,'issues':issues,'minimum_M3_edge_distances_mm':clearances,'minimum_tiles_per_panel':minimum,
    'scope':'Saved CAD/mesh/profile checks only. No physical print, laser cut, gasket torque, hand-access trial, structural or acoustic testing.'}
(ROOT/'validation/interference_report.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert result['all_pass']
