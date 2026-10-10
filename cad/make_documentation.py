"""Build acrylic manufacturing documentation from the checked export metadata."""
from pathlib import Path
from collections import Counter
import json,csv,math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'validation/geometry_report.json').read_text())
v=json.loads((ROOT/'validation/interference_report.json').read_text())
assert v['all_pass']
W,D,H=m['dimensions_mm'];vol=m['volume'];variants=m['variants']
net=variants['a1_mini']['nominal_net_litres']
def write(path,s):(ROOT/path).write_text(s.strip()+'\n')
write('README.md',f'''# Tifa 6 / 10 mm acrylic enclosure

One passive speaker, **220 W x 380 H x {D:.3f} D mm**, six rectangular outer panels, one window brace and M3 assembly. Nominal net volume: **16.100 L acrylic / {net:.3f} L tiled prototype**. Depth excludes projecting drivers, port flange and screw heads.

Retains the SB16PFCR25-4 woofer, SB26ST-C000-5 tweeter and original Tifa 6 crossover. Driver centres are 160 and 324.1 mm above the base. A two-piece printed port retains 50 mm bore, 185 mm assembled axial length and R14 outlet flare. No amplifier compartment.

## Choose one export set

| Set | Sheet parts | Permanent printed fittings | Prototype splice pieces | Physical parts |
|---|---:|---:|---:|---:|
| [Unrestricted acrylic](exports/unrestricted/) | 7 whole panels | 13 | 0 | 20 |
| [A1 mini test build](exports/a1_mini/) | 32 tiles | 13 | 15 | 60 |

Each set contains matching DXF, SVG and 10 mm STL panel profiles, STEP assemblies and a print manifest. Print the A1 set without scaling; all its meshes fit 178 x 178 x 180 mm. The 47 unique STL files include two splice designs printed in quantities 9 and 6. The seven full-panel STLs in the unrestricted set intentionally exceed the A1 mini envelope; its 13 fittings fit.

The assembled panel dimensions, thickness and component locations match. Only the A1 version has prototype seams, extra clearance holes, external splice strips/crosses and eight additional front-rail insert pilots. Use fittings from the selected set; the four front rails differ by those prototype holes. Orange pieces in the A1 render are prototype-only.

## Start here

- [Manufacturing drawings](docs/manufacturing-drawings.pdf)
- [Assembly and seals](docs/assembly-instructions.md), [hardware](docs/fastener-list.md), [printing and cutting](docs/print-settings.md)
- [Panel list](docs/panel-list.csv), [fastener map](docs/fastener-map.csv), [prototype tile map](docs/prototype-tile-map.csv)
- [Fit coupon](exports/calibration/): check actual sheet thickness and kerf before cutting the cabinet
- [Acoustic differences](docs/acoustic-design-notes.md), [verification](docs/dimensional-verification.md)
- [Editable Python CAD](cad/speaker_assembly.py), [parameters](cad/speaker_parameters.json), [FreeCAD assembly](cad/speaker_assembly.FCStd), [renders](renders/)

Use nominal 10 mm acrylic. Cutting profiles are in mm with no kerf compensation. Printed rails carry the M3 inserts; acrylic has clearance holes and compliant flat washers, never threaded or heat-set holes. The rear panel removes for service with the port and crossover attached.

Geometric checks pass. Physical fit, printing, laser cutting, gasket compression, strength and acoustic performance remain untested. The printed prototype checks construction and fit; it does not establish acrylic acoustic behaviour. Component displacement is estimated, so nominal net volume is not a finished-cabinet measurement.

## Rebuild

Install `cad/requirements.txt`. Run `cad/speaker_assembly.py`, then `cad/inspect_geometry.py`, `cad/verify_profiles.py`, `cad/render_views.py` and `cad/make_documentation.py`. The first command replaces the generated export folders. Run `cad/freecad_project.FCMacro` with FreeCAD, followed by `cad/verify_freecad.py`. Python/JSON is the parametric source; FCStd contains editable imported solids and a dimension sheet, not a sketch-based feature history. The sheet layout intentionally targets 220 x 380 mm and 10 mm stock; changing those requires revisiting joins and subdivision. Depth is solved from net volume.
''')
write('docs/assembly-instructions.md',f'''# Assembly / one acrylic enclosure

Coordinates are x across the front, y from front to rear, z above the base. All dimensions are mm. Outside box: 220 x {D:.3f} x 380 (W x D x H). Front is y=0. The rear is removable; the remaining five outer panels form a gasketed, screw-fastened box.

## Preparation and seals

Laser-cut seven 10 mm sheets from the unrestricted profiles, or print the A1 tiles and join them first as described below. Test the 80 x 50 mm coupon before committing to the cabinet. Measure stock and kerf; nominal 10 mm dimensions are not automatically correct for a particular sheet. Check the real drivers, driver screw heads, crossover envelope and inserts. Protect the front panel's narrow 5.4 mm ligament above the tweeter opening until its carrier is fitted.

Install 60 M3 heat-set inserts in the PRINTED fittings while separate. Use 4 mm-long inserts specified for a 4.2 mm pilot in the chosen polymer; most pilots are 5 mm deep, driver pilots 7 mm. Test the insert supplier's fit and retention on scrap. No insert or thread belongs in acrylic. The A1 front rails have eight additional receivers, for 68 inserts total.

All acrylic M3 clearance holes are 4.5 mm. Use flat metal washers over acrylic-compatible cushioning washers; the assumed combined stack under each head is 1.5 mm. Use 9 mm OD at ordinary sheet fixings and port flange, 7 mm OD at the port coupling and prototype splices. Do not countersink. Only tighten enough to seat and seal: torque has not been qualified. Driver screws use heads fitting the original recesses; no extra washer stack is assumed there.

Use acrylic-compatible closed-cell foam and removable non-curing sealant, checking compatibility with the actual sheet grade. The four front/rear perimeter joins and the side-to-top/bottom joins have a 0.5 mm compressed gap. Start with 1 mm foam, 10 mm wide at sheet butt ends, compressed to 0.5 mm. Apply continuous strips around the front and rear mating perimeter, and along top/bottom side-sheet ends. Butt strip ends carefully; use a small amount of compatible removable butyl at corners and T intersections. Foam must bridge each entire wall thickness. Seal around each through screw beneath the cushioning washer. Do not rely on screw pressure alone to close an unsealed gap.

The brace has a 0.5 mm clearance to each inner wall. Fit narrow foam strips around its outer edge to take up that gap and prevent rattle; it transfers load through those contacts and its four rail shelves. It needs no acoustic seal across its open centre. Keep the shelf bearing faces free of thick gasket material so its z=250 mm underside stays on its supports.

## Driver subassembly

The circular acrylic through-holes are 177 mm woofer and 101 mm tweeter. Printed adapter noses are 176 and 100 mm. Wrap each nose in 6 mm-wide, 1 mm-thick closed-cell foam, centred within the acrylic thickness, to compress radially into the 0.5 mm gap. Butt and seal the ends. The rear flanges locate on the panel via four M3 x 16 screws each, with a 0.5 mm thin cushioning gasket at the flange land. Keep this gasket out of the radial seal path.

Join the woofer's two carrier halves at z=160, sealing their 0.2 mm split with a very thin compatible removable sealant. Avoid a step in the seating surface. Its two halves each have two panel fixings and two driver receivers. The tweeter carrier is one piece; its printed terminal relief accommodates the terminal span while the acrylic hole stays circular. Carrier seat depths are 3.6 mm woofer / 3.0 mm tweeter behind the front face. A compressed driver gasket adds its real thickness to the final position; use a thin continuous gasket and verify flushness before tightening the four M3 x 10 screws per driver.

## Port and rear subassembly

Join the port inlet and mouth sections with a 0.5 mm compressed annular gasket (50 mm ID, 72 mm OD, two holes on 64 mm centres), two M3 x 16 screws, 7 mm washers and nuts. Nothing may enter the 50 mm bore. The gasket restores the full 185 mm assembled length. The exterior flange bears on the rear sheet through a 0.5 mm compressed gasket (73 mm ID, 96 mm OD, four holes on 88 mm PCD). Secure with four M3 x 20 screws, head washers/cushions and internal flat washers/nuts. The 72.5 mm spigot fits the 73 mm panel opening. The mouth plane sits 3.5 mm beyond the rear sheet.

Fit the crossover to a 120 x 90 x 2 mm insulating board with 100 x 70 mm mounting-hole pattern. Use four purchased female/female M3 x 20 mm spacers, four M3 x 16 rear screws and four M3 x 6 board screws. The populated assembly must fit x +/-60, z100..190 and 55 mm depth in front of the spacer tips. This is a mounting envelope, not a supplied PCB layout. Keep the manufacturer's circuit, component values, coil specifications and polarity. Fit two insulated binding posts suitable for 8 mm panel holes with their supplied nuts and seals.

## Cabinet assembly order

1. Fit the lower rails to the bottom and sides. Add upper rails and loosely start the side screws. Each corner uses two 179.5 mm rail lengths; integral shelves identify the upper pieces. Front/rear rail names are viewed from the front. Keep the lower/upper end faces aligned at z=190.
2. With the top and front still off, lower the window brace onto the four shelves at z=250. Its central shallow notch faces the front and clears the woofer carrier. Fit four M3 x 16 screws from above. Check its edge foam contacts all four walls when the panels are offered up.
3. Fit the top panel. Square the box with the front/rear panels temporarily offered up, then tighten side and cap screws evenly. Front/rear faces must remain parallel; do not use final tightening to bend acrylic into position.
4. Fit the front panel with its adapters and drivers using eight M3 x 16 rail screws. The brace must be installed first: it cannot be lowered past the fitted driver adapters. Leave rear access open to connect drivers and inspect continuous seals.
5. Fit porous lining in upper side/rear areas, clear of driver backs, shelves and screws. Leave the port inlet region bare. Secure wire with slack for rear-panel removal, clear of the duct and cones.
6. Offer the preassembled rear panel with port and crossover attached. Check leads and seals, then close with eight M3 x 16 rail screws. Its port inlet has {m['port_inlet_to_front_wall_mm']:.2f} mm clear approach to the front inner wall. Maintain this space; no loose foam or wiring in the inlet.
7. Check gaps, rocking, driver seating and fastener engagement. Conduct a gentle low-frequency leak check and repair seals rather than overtightening acrylic. Measure impedance/tuning, response through crossover and panel vibration before treating it as acoustically qualified.

## A1 prototype only

Build each sheet from its numbered tiles on a flat surface before the steps above. Tiles use 0.5 mm seams, with 1 mm foam compressed to 0.5 mm through the 10 mm thickness; seal all seam intersections, including where seams reach adapter radial seals. Join using nine straight strips and six crosses, all 4 mm thick. All outer-sheet splices are OUTSIDE; the four brace strips lie on top of the brace. Use 42 M3 x 20 screws. Thirty-four use inner 7 mm washers and nuts; eight front-edge strip screws enter the additional front-rail inserts and are fitted when the front meets the rails. The separate front pieces can be loosely held for handling by their driver carriers until the rail screws are installed.

Positions: front strips at x=+/-96,z125 and270, plus x=0,z35; rear crosses x=0,z125 and280; one cross at the centre of each side/top/bottom. Four brace strips bridge its frame at the middle of each edge. Use `prototype-tile-map.csv` and `fastener-map.csv` for exact locations. The brace's four pieces must be joined before installing it. These seams and fittings are prototype-only and are absent from unrestricted sheets. Do not substitute production front rails if you need the prototype receivers.

## Service and evidence limits

Undo the eight rear perimeter screws and withdraw the rear panel backwards with its port/crossover attached. Leave sufficiently long leads or disconnect labelled connectors before fully removing it. Driver replacement is from the front; adapter replacement is easiest with the rear open. All structural joints are reversible.

Screw paths and final component envelopes are checked digitally. The proposed sequence provides open top/front/rear access during installation, but real hand access, tool use, gasket compression, insert pull-out strength and sheet behaviour require a dry assembly. There are no qualified load or tightening-torque ratings.
''')
write('docs/print-settings.md','''# Printing and laser cutting

## Whole acrylic sheets

Use `exports/unrestricted/laser/`: seven DXFs or seven equivalent SVGs, one of each. All profiles are millimetres, nominal 10 mm thickness, with uncompensated cut centre-lines. No nesting, laser power or feed settings are supplied. Have the fabricator select settings for the actual acrylic grade and machine. Do not cut both DXF and SVG duplicates. Matching panel STLs are exact 10 mm extrusions of those profiles before print orientation.

Cut the optional 80 x 50 mm coupon first. It has 4.5 / 4.7 / 5.0 mm holes left to right and 10.0 / 10.2 / 10.4 mm-wide slots. Measure the sheet, holes and slots; check screw clearance, cushioning washers and a sample rail. Confirm effective laser kerf with the fabricator and apply compensation there, not twice. If stock differs materially from 10 mm, revise the CAD joins and screw stack, then regenerate rather than scaling files. Remove residue and deburr without changing functional dimensions. Protect the narrow tweeter top ligament during handling.

Acrylic M3 holes are 4.5 mm with centres at least 1.5 hole diameters (6.75 mm) from cut edges. Follow the sheet maker's drilling/fastening guidance and the supplied source links. Oversize clearance accommodates movement; fasteners bear on compliant flat washers. No countersinks or heat-set inserts in acrylic.

## A1 mini prototype

Use only `exports/a1_mini/stl/` and its print manifest. Print one of every file except `splice_strip.stl` (9) and `splice_cross.stl` (6). There are 47 unique files / 60 physical pieces. Do not scale. Eight side tiles print upright on a 10 mm edge, reaching 179.25 mm high; all other sheet tiles print flat. The four-piece side subdivision wins over six flat tiles. All other panels use the fewest regular rectangular subdivisions among checked flat/upright axis-aligned layouts, preferring flat printing when counts tie.

The corresponding tile DXF/SVG files describe exactly the same panel profiles if a tiled sheet test is preferred. Tile names encode parent panel and column/row, with offsets in `prototype-tile-map.csv`. This is a construction prototype: tiled plastic is not an acoustic substitute for the acrylic cabinet.

## Permanent fittings (both sets)

Eight rails, two woofer-carrier halves, one tweeter carrier and two port pieces all fit the A1 mini. Saved STL orientation is already on the bed. Rails print side-face down diagonally on the plate. Adapters print rear-flange down. Port pieces print with their larger end face on the bed. Keep the long bore clear of unnecessary supports.

Most geometry needs no supports, but local supports are required under projecting adapter noses and near the port mouth's flare throat. Small horizontal holes may need cleanup. Inspect these areas in the slicer and remove supports while the parts are separate. A slicer toolpath and physical support removal have not been verified.

Starting settings: PETG, 0.4 mm nozzle, 0.2 mm layers, six perimeters, six top/bottom layers. Use solid material at rails, insert seats, adapters, splice pieces and brace; the thin duct wall fills with perimeters. For large test panels, 40-50% infill with solid zones around screws and driver openings can reduce material while retaining 10 mm outer thickness. This is a fit-prototype starting point, not an acoustically or structurally qualified infill recipe. Print the coupon before the full set.

Use a brim for the tall side tiles if the slicer confirms it fits. Check all support/brim/purge footprints within the real bed; passing mesh dimensions alone does not establish this. Do not exceed the 178 x 178 x 180 mm part envelope. Obtain filament and time estimates from the actual sliced plates. Check every sealing face for flatness, layer leaks and elephant foot.
''')
counts=Counter((b['label'],b['length']) for b in m['bolts'])
hardware=[(32,'M3 x 16 screw','Side/front/rear to rails'),(8,'M3 x 16 screw','Top/bottom to rails'),(4,'M3 x 16 screw','Brace to shelves'),(8,'M3 x 16 screw','Adapters to front'),(4,'M3 x 16 screw','Rear to crossover spacers'),(2,'M3 x 16 screw','Port coupling'),(8,'M3 x 10 screw','Drivers'),(4,'M3 x 20 screw','Port flange'),(4,'M3 x 6 screw','Crossover board'),(60,'M3 heat-set insert, 4 mm long','Printed fittings; 4.2 mm pilots'),(6,'M3 plain nut','Port flange and coupling'),(64,'9 mm OD M3 flat washer','60 sheet-side heads + 4 port flange rear washers'),(60,'Compatible cushioning washer','Sheet-side heads; metal+cushion stack 1.5 mm'),(4,'7 mm OD M3 flat washer','Both ends of 2 port-coupling screws'),(4,'M3 female/female 20 mm spacer','Crossover'),(2,'Insulated binding post for 8 mm opening','Own nuts and seals'),(1,'120 x 90 x 2 insulating board','100 x 70 mm mounting pattern')]
# 60 sheet heads = 40 box + 4 brace + 8 adapters + 4 spacer + 4 flange.
extra=[(42,'M3 x 20 screw','Prototype splices'),(8,'M3 heat-set insert, 4 mm long','Additional front-rail pilots'),(34,'M3 plain nut','Prototype splices except 8 front-rail receivers'),(76,'7 mm OD M3 flat washer','42 heads + 34 nuts'),(42,'Compatible cushioning washer','Prototype heads; total head washer stack 1.5 mm')]
write('docs/fastener-list.md','''# Hardware for one enclosure

Production: **74 M3 screws** (58 x M3-16, 8 x M3-10, 4 x M3-20, 4 x M3-6), 60 inserts and 6 nuts. Lengths are under-head dimensions in mm. Use ordinary socket/button heads, never countersunk; verify head fit in the real driver recesses.

| Qty | Item | Purpose |
|---:|---|---|
'''+ '\n'.join(f'| {q} | {n} | {use} |' for q,n,use in hardware)+'''

## A1 prototype additions

The same base hardware plus the following. Totals: **116 screws, 68 inserts, 40 nuts**.

| Extra qty | Item | Purpose |
|---:|---|---|
'''+ '\n'.join(f'| {q} | {n} | {use} |' for q,n,use in extra)+'''

Also supply compatible closed-cell foam, thin driver gaskets, compatible removable sealant, porous lining and wire. Port coupling washer stack is 1.5 mm at the head; combine a flat washer with a suitable spacer washer as needed. Prototype and port nut-side washer+nut allowance is 3 mm. Select actual hardware to those stack heights; changing them changes engagement. Keep inserts flush at the receiver entry. No qualified tightening torque is supplied.

Production acrylic parts: 7. Permanent printed fittings: 13. Prototype: 32 sheet tiles + the same 13 fittings + 9 strips + 6 crosses. Binding-post hardware and electronic crossover components are additional to the M3 counts above.
''')
with (ROOT/'docs/mechanical-hardware.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['set','quantity','item','purpose']);w.writerows([['production',*x] for x in hardware]+[['prototype_additional',*x] for x in extra])
with (ROOT/'docs/fastener-map.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['set','index','purpose','length_mm','head_x','head_y','head_z','axis_x','axis_y','axis_z','insert_receiver'])
 for group,key in [('both','bolts'),('PROTOTYPE ONLY','prototype_bolts')]:
  for i,b in enumerate(m[key],1):w.writerow([group,i,b['label'],b['length'],*b['start'],*b['axis'],b['receiver'] or 'nut_or_spacer'])
with (ROOT/'docs/panel-list.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['part','width_mm','height_mm','thickness_mm','quantity'])
 for n,p in m['panel_profiles'].items():w.writerow([n,*p['size'],10,1])
with (ROOT/'docs/prototype-tile-map.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['tile','parent_panel','offset_u_mm','offset_v_mm','size_u_mm','size_v_mm','thickness_mm'])
 for n,p in m['prototype_tiles'].items():w.writerow([n,p['parent'],*p['offset'],*p['size'],10])
for old in ['docs/joint-map.csv','docs/print-manifest.csv']:(ROOT/old).unlink(missing_ok=True)
fb=343/(2*math.pi)*math.sqrt(math.pi*.025**2/(.0161*(.185+1.46*.025)))
write('docs/acoustic-design-notes.md',f'''# Acoustic baseline and volume

Retain the original SB16PFCR25-4, SB26ST-C000-5 and Tifa 6 passive crossover exactly as specified in the included manufacturer references. Preserve component values, coil specifications and polarity. This revision does not redesign the crossover or claim an optimised response.

Driver centres remain on the centreline at drawing coordinates z160 and z324.1, spacing 164.1 mm. Adapter seating depths are 3.6 and 3.0 mm. The rectangular baffle is 220 mm wide and vertical; the original tapered cabinet is approximately 220 mm wide at the base / 180 mm at the top with a 6 degree lean. The changed width, edges and tilt change diffraction, baffle step and time alignment. The same crossover therefore does not guarantee the same tonal balance or crossover summation.

The port retains a 50 mm bore, 185 mm mouth-to-inlet axial length and R14 outlet flare. Its centre is at rear z55, versus approximately z307.5 in the original. The inlet has {m['port_inlet_to_front_wall_mm']:.3f} mm axial clearance to the front wall (greater than its bore), and its bore edge is 20 mm above the floor. Keep that area unlined and clear of wires. Different wall loading and flare end effects can shift tuning. The original nominal tuning is about 37 Hz; a simplified straight-cylinder Helmholtz estimate using 343 m/s and 0.85r + 0.61r end corrections is {fb:.1f} Hz. Neither is a prediction validated for this acrylic build. Measure impedance and near-field port output before adjusting length or claiming a tuning frequency.

## Nominal volume ledger, litres

| Item | Acrylic |
|---|---:|
'''+ '\n'.join(f'| {k.replace("_litres","").replace("_"," ")} | {value:.6f} |' for k,value in vol.items())+f'''

The production air solid deducts physical CAD fittings and brace, port duct air, estimated driver material, 0.120 L crossover material, spacers, wire and 0.010 L hardware. The crossover clearance envelope is not treated as solid material. Driver shapes are approximate displacement proxies, not exact manufacturer CAD.

The A1 net is calculated separately from its saved air solid: **{net:.6f} L**. It restores brace material removed by prototype seams/holes and additional receiver holes, deducts the four internal brace straps and a further 0.004 L prototype hardware allowance. Outer sheet splices are outside the cavity. Small seam/foam effects are nominally sealed by the specified gaskets. Hardware and electronics allowances remain estimates; actual installed net volume can vary by a few tenths of a litre. The many displayed digits describe CAD arithmetic, not physical measurement accuracy.

10 mm acrylic, braced at z250..260, differs in stiffness and damping from the original wood cabinet. The frame rails and single four-wall brace provide structural support but no panel-resonance, load or fatigue analysis has qualified the result. Do not remove the brace. The printed tiled prototype verifies fit and construction only; its seams, infill and polymer do not establish acrylic acoustic performance.

Apply porous lining in upper side/rear regions without obstructing the port or drivers. After assembling the actual acrylic cabinet, check air leaks, impedance/tuning, near-field bass, response through the crossover and panel vibration. Physical acoustic validation remains outstanding.
''')
write('docs/dimensional-verification.md',f'''# Verification scope

Current automated checks pass in `validation/interference_report.json`; native FreeCAD validation is in `freecad_report.json`.

- Cabinet 220 x {D:.6f} x 380 mm (W x D x H), nominal 10 mm panels; modelled compressed outer gasket gap 0.5 mm.
- Seven full sheet profiles and 32 prototype tile profiles export as DXF/SVG and matching extruded STL. DXFs were reimported and extruded; symmetric volume difference from source is below 0.05 mm3. SVG line/circle/arc coordinates, direction, scale and viewport were independently compared to saved DXFs in `profile_report.json`.
- Every saved STL is one connected, consistently oriented, watertight positive-volume mesh. Permanent fittings in both sets and all prototype parts fit 178 x 178 x 180 mm. Whole unrestricted sheet STLs are deliberately exempt from A1 fit.
- Sheet thickness is 10 mm before orientation. Upright side tiles are 179.25 mm high; the print manifest records each oriented bounding box.
- No final-position panel/fitting or component-envelope intersections. Conservative woofer rear envelope is clear; tweeter terminal relief clears the supplied terminal proxy.
- 74 production / 116 prototype M3 screw paths, head and washer envelopes clear. Insert pilots and nominal thread engagement/bottom clearance checked. Actual insert maker, washer stack and driver heads must match the model assumptions.
- Port has 50 mm straight bore, 185 mm assembled length and {m['port_inlet_to_front_wall_mm']:.3f} mm clear axial inlet approach. Flange and coupling align.
- Production net 16.100000 L; prototype net {net:.6f} L, including extra internal prototype material and hardware allowance.
- Acrylic 4.5 mm M3 holes meet the 6.75 mm minimum centre-to-edge rule, including openings. Prototype nut/washer envelopes clear the parts and components.
- Tile counts are minimum among regular rectangular flat/upright, axis-aligned subdivisions of each panel's bounding rectangle, choosing flat when counts tie. This is not a proof over arbitrary diagonal or irregular cutting schemes.
- FreeCAD contains 20 production parts, 60 prototype instances and four component references (84 shapes); saved native shapes are checked against exported STEP volumes.

Gasket routing and assembly order were reviewed against the CAD. Continuous seals require correct fitting at corners, carrier splits and prototype T intersections. There is no simulated seal compression, deformation, toolpath, hand-access trial, insert load test, leak test or measured acoustic response. 'Printable' here means valid geometry and envelope fit, with documented local support needs; it is not a completed physical print qualification.
''')
# Landscape drawing pack, readable without software; exact profiles remain manufacturing authority.
c=canvas.Canvas(str(ROOT/'docs/manufacturing-drawings.pdf'),pagesize=landscape(A4));PW,PH=landscape(A4)
def txt(x,y,s,size=10):c.setFont('Helvetica',size);c.drawString(x,y,str(s))
def lines(x,y,rows,size=10,step=20):
 for row in rows:txt(x,y,row,size);y-=step

def head(title,sub,page):
 txt(32,PH-38,title,20);txt(32,PH-58,sub,10)
 txt(32,20,'TIFA ACRYLIC DERIVATIVE | mm | Nominal stock / zero kerf compensation | Physical qualification outstanding',8)
 txt(PW-70,20,f'{page} / 5',8)
head('01 / One box, matching manufacturing sets',f'220 W x 380 H x {D:.3f} D | 10 mm panels | 16.100 L nominal net',1)
s=.74;b=164
for x,label in [(48,'FRONT'),(302,'SIDE SECTION'),(601,'REAR')]:txt(x,478,label,11)
c.rect(48,b,220*s,380*s)
for z,opening,driver,pcd in [(160,177,176,165),(324.1,101,100,88.5)]:
 c.circle(48+110*s,b+z*s,opening*s/2)
 c.setDash(2,2);c.circle(48+110*s,b+z*s,driver*s/2);c.setDash()
 for a in [45,135,225,315]:c.circle(48+(110+pcd/2*math.cos(math.radians(a)))*s,b+(z+pcd/2*math.sin(math.radians(a)))*s,1.5*s)
c.rect(302,b,D*s,H*s);c.rect(302+10*s,b+10*s,(D-20)*s,360*s)
c.rect(302+11*s,b+250*s,(D-22)*s,10*s)
c.rect(302+(D+3.5-185)*s,b+30*s,185*s,50*s)
c.rect(601,b,220*s,380*s)
for dia in [50,73,96]:c.circle(601+110*s,b+55*s,dia*s/2)
for x in [-15,15]:c.circle(601+(110+x)*s,b+225*s,4*s)
lines(48,144,['Centres: z160 / z324.1','177 / 101 acrylic through-holes'],9)
lines(302,144,['Brace underside z250, thickness10','Port axis z55; 50 ID x 185 assembled'],9)
lines(601,144,['Rear removes with port + crossover','Two 8 mm binding-post openings'],9)
lines(32,85,['Driver seats are in printed adapters: woofer depth3.6, tweeter3.0; 165 / 88.5 PCD at 45 + 90n degrees.',
 'Circular acrylic openings stay simple. Printed tweeter terminal relief: 81.8 x 13; centre bore73.',
 'Dimensioned profiles are in DXF/SVG. Cabinet depth excludes the port flange, driver protrusions and screw heads.'],9,17)
c.showPage()
head('02 / Seven sheets + thirteen printed fittings','Unrestricted acrylic build / 20 manufactured pieces / 74 M3 screws',2)
c.drawImage(str(ROOT/'renders/exploded.png'),22,195,width=451,height=316,mask='auto')
y=470
for n,p in m['panel_profiles'].items():txt(490,y,f'{n.upper():8}  {p["size"][0]:.3f} x {p["size"][1]:.3f} x 10',10);y-=25
lines(490,256,['8 rails, 179.5 long each','2 woofer adapter halves','1 tweeter adapter','2 port pieces'],10,24)
lines(32,160,['All outer panels use plain butt joints and 0.5 mm compressed gasket gaps.',
 'Printed rails carry M3 inserts. Upper rails integrate the four brace shelves; no separate shelf brackets.',
 'Brace has 30 mm frame, corner rail cutouts and a shallow front notch to clear the woofer carrier.',
 'Use all seven whole-panel DXFs OR SVGs, one each. Whole-panel STLs reproduce exactly those 10 mm profiles.',
 'Test actual thickness and kerf with the supplied 80 x 50 fit coupon before cutting these panels.',
 'The top tweeter ligament is only 5.4 mm: protect during handling and fit its supporting carrier.'],10,20)
c.showPage()
head('03 / A1 mini: identical size, prototype-only seams','32 sheet tiles + 13 fittings + 15 joining pieces = 60 prints / 47 unique STL files',3)
# Accurate subdivision diagrams; holes omitted here to make cut placement readable.
x=38;ybase=210
for n in ['front','rear','left','top','brace']:
 p=m['panel_profiles'][n];a,bp=p['size'];scale=.43 if n in ['front','rear','left'] else .52
 width=a*scale;hh=bp*scale
 txt(x,ybase+hh+14,n.upper(),10);c.rect(x,ybase,width,hh)
 xs,ys=m['prototype_cuts'][n];c.setDash(3,2)
 for u in xs[1:-1]:c.line(x+u*scale,ybase,x+u*scale,ybase+hh)
 for vv in ys[1:-1]:c.line(x,ybase+vv*scale,x+width,ybase+vv*scale)
 c.setDash();txt(x,ybase-20,f'{len(xs)-1} x {len(ys)-1} tiles',9);x+=width+40
lines(38,470,['Front 6, rear 6, left 4, right 4, top 4, bottom 4, brace 4.',
 'Side tiles print upright (179.25 high); other sheet tiles print flat. Saved STLs are already oriented.',
 'Right matches left subdivision; bottom matches top. Dashed lines are 0.5 mm gasketed prototype seams.'],10,22)
lines(38,154,['Print splice_strip.stl 9 times and splice_cross.stl 6 times; every other STL once.',
 'All outer-panel splices are external. Four brace strips lie on its upper face. Extra holes are prototype-only.',
 'Use the A1 front rails: they contain eight additional insert pilots for the front-edge strips.',
 'Tile DXFs/SVGs match the tile STLs, not the unsplit full sheet. Exact offsets are in prototype-tile-map.csv.',
 'Never scale to fit. Check brims, supports and purge paths in the slicer; the side tiles are tall, narrow prints.',
 'A construction prototype does not establish acrylic panel stiffness, damping or acoustic performance.'],10,19)
c.showPage()
head('04 / M3 joints, seals and assembly access','No countersinks or threads in acrylic / rear panel is the service panel',4)
lines(36,485,['PRODUCTION HARDWARE','58 x M3-16, 8 x M3-10','4 x M3-20, 4 x M3-6','60 inserts, M3 x4 long','6 M3 nuts; 4 M3 x20 spacers','', 'PROTOTYPE ADDITIONS','42 x M3-20, 8 inserts, 34 nuts','9 strips + 6 crosses','See hardware list for washer counts.'],11,26)
lines(350,485,['JOINT ASSUMPTIONS','Acrylic holes4.5 / insert pilots4.2','Flat washer + cushion stack1.5','M3 insert engagement checked in CAD','Compressed sheet / port gasket0.5','Adapter radial clearance0.5','Woofer adapter split0.2','Driver gaskets thin and continuous','Check actual hardware before assembly.'],11,26)
lines(36,182,['1. Fit inserts in printed parts. Join prototype tiles first if using the A1 set.',
 '2. Assemble bottom, sides and rails. Lower the brace onto shelves and fasten it from above.',
 '3. Fit top, square the box, then fit the front panel with its driver carriers. Brace must go in first.',
 '4. Fit rear port, crossover/spacers and binding posts separately; connect leads with service slack.',
 '5. Close the rear with eight perimeter screws. Seal corners, screw holes and every gasket intersection.',
 '6. Dry-fit, leak-test and measure. Rear service: remove eight perimeter screws and withdraw backwards.',
 'Detailed seal routes, port gaskets and adapter assembly are in assembly-instructions.md.'],10,20)
c.showPage()
head('05 / Volume and validation','Unrestricted acrylic 16.100 L / A1 construction prototype 16.092 L nominal',5)
y=480
for k,value in vol.items():txt(34,y,k.replace('_litres','').replace('_',' '),10);txt(303,y,f'{value:.6f} L',10);y-=25
lines(442,480,['DIGITALLY CHECKED','Manifold meshes / single CAD solids','A1 envelope fit in supplied orientations','2D profile / 10 mm extrusion agreement','Screw, head, washer and insert clearances','No part or component-envelope collisions','Port fit and clear inlet approach','Minimum rectangular tile counts','84 native shapes checked against STEP'],10,25)
lines(34,186,['Volume uses estimated driver, electronics and hardware displacement; installed net volume will differ.',
 'The flat 220 mm baffle differs from the original tapered 180-220 mm, 6 degree tilted baffle.',
 'Diffraction, crossover summation and panel resonances may change. Retain the original crossover initially.',
 f'Port: original nominal37 Hz; simplified cylinder estimate{fb:.1f} Hz. Neither validates this cabinet tuning.',
 'Outstanding: physical fit, gasket compression, insert strength, slicing, support removal, leakage and sound.',
 'Follow the included manufacturer references and acrylic fabrication guidance before production cutting.'],10,21)
c.save();print('Generated acrylic documentation and five-page drawing pack')
