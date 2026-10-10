# Laser cutting and printed fittings

## Acrylic panels

Use `exports/current/laser/`: seven DXFs or the equivalent seven SVGs, one of each. Choose one file format, not both. Six pieces form the outer box; the seventh is the internal window brace. All profiles are millimetres, nominal 10 mm stock and uncompensated for kerf.

Front and rear are 220 x 380 mm; sides 241.652 x 359 mm; top/bottom 220 x 241.652 mm; brace 199 x 240.652 mm. Cut the optional coupon in `exports/calibration/` first. Confirm actual sheet thickness, screw clearance and kerf with the fabricator. Do not scale the design to compensate for different stock thickness.

The seven corresponding flat STLs are identical profile extrusions, 10 mm thick and already lying on the bed. They have no additional seams or joining holes. Their purpose is to provide a solid version of the laser-cut sheets.

Protect the narrow acrylic ligament above the tweeter opening until its supporting adapter is fitted. Use flat washers and acrylic-compatible cushioning seals, not countersunk screws. No threads or heat-set inserts go in acrylic. Follow the manufacturer fabrication guidance in the source register.

## Printed enclosure fittings

Print each fitting once: eight rail pieces, two woofer-adapter halves, one tweeter adapter and `bass_reflex_port.stl`. See the `printed_fitting` rows in `exports/current/print-manifest.csv`. Files are millimetres and already oriented; use 100% scale.

Starting settings: PETG, 0.4 mm nozzle, 0.2 mm layers, six perimeters and six top/bottom layers. Use solid material around inserts, driver seats and brace supports. Check sealing faces for warping and layer leaks. These settings require a physical fit check; insert retention and torque are not qualified.

Rail STLs lie side-down diagonally. Adapters lie rear-flange-down and need local support under projecting noses. The continuous port is 96 x 96 x 185 mm, flange on the bed; inspect local supports at the flare throat. Keep the long vertical bore free of unnecessary support and clean it fully before assembly. Check slicer-generated supports and support removal before printing.
