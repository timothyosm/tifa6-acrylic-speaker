> Historical split-port / A1 reference. For the current whole-panel build with one-piece port, use [current instructions](current/assembly-instructions.md).

# Verification scope

Current automated checks pass in `validation/interference_report.json`; native FreeCAD validation is in `freecad_report.json`.

- Cabinet 220 x 262.652160 x 380 mm (W x D x H), nominal 10 mm panels; modelled compressed outer gasket gap 0.5 mm.
- Seven full sheet profiles and 32 prototype tile profiles export as DXF/SVG and matching extruded STL. DXFs were reimported and extruded; symmetric volume difference from source is below 0.05 mm3. SVG line/circle/arc coordinates, direction, scale and viewport were independently compared to saved DXFs in `profile_report.json`.
- Every saved STL is one connected, consistently oriented, watertight positive-volume mesh. Permanent fittings in both sets and all prototype parts fit 178 x 178 x 180 mm. Whole unrestricted sheet STLs are deliberately exempt from A1 fit.
- Sheet thickness is 10 mm before orientation. Upright side tiles are 179.25 mm high; the print manifest records each oriented bounding box.
- No final-position panel/fitting or component-envelope intersections. Conservative woofer rear envelope is clear; tweeter terminal relief clears the supplied terminal proxy.
- 74 production / 116 prototype M3 screw paths, head and washer envelopes clear. Insert pilots and nominal thread engagement/bottom clearance checked. Actual insert maker, washer stack and driver heads must match the model assumptions.
- Port has 50 mm straight bore, 185 mm assembled length and 71.152 mm clear axial inlet approach. Flange and coupling align.
- Production net 16.100000 L; prototype net 16.091519 L, including extra internal prototype material and hardware allowance.
- Acrylic 4.5 mm M3 holes meet the 6.75 mm minimum centre-to-edge rule, including openings. Prototype nut/washer envelopes clear the parts and components.
- Tile counts are minimum among regular rectangular flat/upright, axis-aligned subdivisions of each panel's bounding rectangle, choosing flat when counts tie. This is not a proof over arbitrary diagonal or irregular cutting schemes.
- FreeCAD contains 20 production parts, 60 prototype instances and four component references (84 shapes); saved native shapes are checked against exported STEP volumes.

Gasket routing and assembly order were reviewed against the CAD. Continuous seals require correct fitting at corners, carrier splits and prototype T intersections. There is no simulated seal compression, deformation, toolpath, hand-access trial, insert load test, leak test or measured acoustic response. 'Printable' here means valid geometry and envelope fit, with documented local support needs; it is not a completed physical print qualification.
