# Assembly / current whole-panel build

Coordinates are x across the front, y from front to rear, z above the base. All dimensions are mm. Outside box: 220 x 262.652 x 380 (W x D x H). Front is y=0. The rear is removable; the remaining five outer panels form a gasketed, screw-fastened box.

## Preparation and seals

Laser-cut the seven 10 mm sheets from `exports/current/laser/`. Print the 12 fittings from `exports/current/stl/`; the seven flat panel STLs in that folder are matching dimensional references. Test the 80 x 50 mm coupon before committing to the cabinet. Measure stock and kerf; nominal 10 mm dimensions are not automatically correct for a particular sheet. Check the real drivers, driver screw heads, crossover envelope and inserts. Protect the front panel's narrow 5.4 mm ligament above the tweeter opening until its carrier is fitted.

Install 60 M3 heat-set inserts in the PRINTED fittings while separate. Use 4 mm-long inserts specified for a 4.2 mm pilot in the chosen polymer; most pilots are 5 mm deep, driver pilots 7 mm. Test the insert supplier's fit and retention on scrap. No insert or thread belongs in acrylic.

All acrylic M3 clearance holes are 4.5 mm. Use flat metal washers over acrylic-compatible cushioning washers; the assumed combined stack under each head is 1.5 mm. Use 9 mm OD at ordinary sheet fixings and the port flange. Do not countersink. Only tighten enough to seat and seal: torque has not been qualified. Driver screws use heads fitting the original recesses; no extra washer stack is assumed there.

Use acrylic-compatible closed-cell foam and removable non-curing sealant, checking compatibility with the actual sheet grade. The four front/rear perimeter joins and the side-to-top/bottom joins have a 0.5 mm compressed gap. Start with 1 mm foam, 10 mm wide at sheet butt ends, compressed to 0.5 mm. Apply continuous strips around the front and rear mating perimeter, and along top/bottom side-sheet ends. Butt strip ends carefully; use a small amount of compatible removable butyl at corners and T intersections. Foam must bridge each entire wall thickness. Seal around each through screw beneath the cushioning washer. Do not rely on screw pressure alone to close an unsealed gap.

The brace has a 0.5 mm clearance to each inner wall. Fit narrow foam strips around its outer edge to take up that gap and prevent rattle; it transfers load through those contacts and its four rail shelves. It needs no acoustic seal across its open centre. Keep the shelf bearing faces free of thick gasket material so its z=250 mm underside stays on its supports.

## Driver subassembly

The circular acrylic through-holes are 177 mm woofer and 101 mm tweeter. Printed adapter noses are 176 and 100 mm. Wrap each nose in 6 mm-wide, 1 mm-thick closed-cell foam, centred within the acrylic thickness, to compress radially into the 0.5 mm gap. Butt and seal the ends. The rear flanges locate on the panel via four M3 x 16 screws each, with a 0.5 mm thin cushioning gasket at the flange land. Keep this gasket out of the radial seal path.

Join the woofer's two carrier halves at z=160, sealing their 0.2 mm split with a very thin compatible removable sealant. Avoid a step in the seating surface. Its two halves each have two panel fixings and two driver receivers. The tweeter carrier is one piece; its printed terminal relief accommodates the terminal span while the acrylic hole stays circular. Carrier seat depths are 3.6 mm woofer / 3.0 mm tweeter behind the front face. A compressed driver gasket adds its real thickness to the final position; use a thin continuous gasket and verify flushness before tightening the four M3 x 10 screws per driver.

## Port and rear subassembly

Use the single `bass_reflex_port.stl`: 50 mm bore, 185 mm mouth-to-inlet length and R14 outlet flare. No coupling gasket, coupling bolts or coupling nuts are needed. The exterior flange bears on the rear sheet through a 0.5 mm compressed gasket (73 mm ID, 96 mm OD, four holes on 88 mm PCD). Secure with four M3 x 20 screws, head washers/cushions and internal flat washers/nuts. The 72.5 mm spigot fits the 73 mm panel opening. The mouth plane sits 3.5 mm beyond the rear sheet.

Fit the crossover to a 120 x 90 x 2 mm insulating board with 100 x 70 mm mounting-hole pattern. Use four purchased female/female M3 x 20 mm spacers, four M3 x 16 rear screws and four M3 x 6 board screws. The populated assembly must fit x +/-60, z100..190 and 55 mm depth in front of the spacer tips. This is a mounting envelope, not a supplied PCB layout. Keep the manufacturer's circuit, component values, coil specifications and polarity. Fit two insulated binding posts suitable for 8 mm panel holes with their supplied nuts and seals.

## Cabinet assembly order

1. Fit the lower rails to the bottom and sides. Add upper rails and loosely start the side screws. Each corner uses two 179.5 mm rail lengths; integral shelves identify the upper pieces. Front/rear rail names are viewed from the front. Keep the lower/upper end faces aligned at z=190.
2. With the top and front still off, lower the window brace onto the four shelves at z=250. Its central shallow notch faces the front and clears the woofer carrier. Fit four M3 x 16 screws from above. Check its edge foam contacts all four walls when the panels are offered up.
3. Fit the top panel. Square the box with the front/rear panels temporarily offered up, then tighten side and cap screws evenly. Front/rear faces must remain parallel; do not use final tightening to bend acrylic into position.
4. Fit the front panel with its adapters and drivers using eight M3 x 16 rail screws. The brace must be installed first: it cannot be lowered past the fitted driver adapters. Leave rear access open to connect drivers and inspect continuous seals.
5. Fit porous lining in upper side/rear areas, clear of driver backs, shelves and screws. Leave the port inlet region bare. Secure wire with slack for rear-panel removal, clear of the duct and cones.
6. Offer the preassembled rear panel with port and crossover attached. Check leads and seals, then close with eight M3 x 16 rail screws. Its port inlet has 71.15 mm clear approach to the front inner wall. Maintain this space; no loose foam or wiring in the inlet.
7. Check gaps, rocking, driver seating and fastener engagement. Conduct a gentle low-frequency leak check and repair seals rather than overtightening acrylic. Measure impedance/tuning, response through crossover and panel vibration before treating it as acoustically qualified.

## Service and evidence limits

Undo the eight rear perimeter screws and withdraw the rear panel backwards with its port/crossover attached. Leave sufficiently long leads or disconnect labelled connectors before fully removing it. Driver replacement is from the front; adapter replacement is easiest with the rear open. All structural joints are reversible.

Screw paths and final component envelopes are checked digitally. The proposed sequence provides open top/front/rear access during installation, but real hand access, tool use, gasket compression, insert pull-out strength and sheet behaviour require a dry assembly. There are no qualified load or tightening-torque ratings.

The parts manifest contains seven flat sheet STLs and 12 fitting STLs. Cut the seven acrylic sheets and print only the fittings. The supplied flat panel STLs match the cutting profiles at 10 mm thickness.
