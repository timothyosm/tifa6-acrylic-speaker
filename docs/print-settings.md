> Historical split-port / A1 reference. For the current whole-panel build with one-piece port, use [current instructions](current/assembly-instructions.md).

# Printing and laser cutting

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
