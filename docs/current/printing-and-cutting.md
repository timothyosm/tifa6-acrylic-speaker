# Printing and cutting the current build

Use `exports/current/print-manifest.csv`. All 19 STLs are millimetres and are already oriented on the bed. Print one of each at 100% scale for a complete test assembly. Printer size is unrestricted. No A1 tiles or splice strips are needed.

For a panel/port geometry check only, print the seven panels plus `bass_reflex_port.stl` (eight pieces). Those eight alone do not include the driver seats or M3 corner supports; the remaining 11 fittings are needed for the assembled enclosure.

For final acrylic construction, laser-cut seven panels from `exports/current/laser/` and print the 12 fittings. DXF and SVG are equivalent outlines; choose one format. The nominal stock is 10 mm, and profiles have no kerf compensation. Cut the optional fit coupon in `exports/calibration/` first and confirm measured stock thickness and kerf with the fabricator. Do not scale a panel to compensate for different stock thickness.

The flat panel STLs are extrusions of the same profiles. Front and rear are 220 x 380 mm, sides 241.652 x 359 mm, top/bottom 220 x 241.652 mm, brace 199 x 240.652 mm; all are 10 mm thick. Protect the narrow acrylic ligament above the tweeter opening until its supporting adapter is fitted.

Starting print settings: PETG, 0.4 mm nozzle, 0.2 mm layers, six perimeters and six top/bottom layers. Use solid regions at inserts, driver seats, brace and screw holes. Large test panels can use 40-50% infill for construction checks; this is not a measured acoustic or structural recipe. Check sealing faces for warping, elephant foot and layer leaks.

Rail STLs lie side-down diagonally. Driver adapters lie rear-flange-down and need local support under projecting noses. The one-piece port is 96 x 96 x 185 mm with its flange on the bed; preview local supports at the flare throat. Leave the long vertical bore free of unnecessary support and clean it completely before assembly. Slicer-added brims, supports and actual support removal need inspection; no physical print has been performed.

Use flat washers and acrylic-compatible cushioning seals, not countersunk screws. All acrylic threads are avoided: heat-set inserts belong only in the printed fittings. Follow the acrylic maker's fabrication guidance linked in the source register.
