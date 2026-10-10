> Historical split-port / A1 reference. For the current whole-panel build with one-piece port, use [current instructions](current/assembly-instructions.md).

# Acoustic baseline and volume

Retain the original SB16PFCR25-4, SB26ST-C000-5 and Tifa 6 passive crossover exactly as specified in the included manufacturer references. Preserve component values, coil specifications and polarity. This revision does not redesign the crossover or claim an optimised response.

Driver centres remain on the centreline at drawing coordinates z160 and z324.1, spacing 164.1 mm. Adapter seating depths are 3.6 and 3.0 mm. The rectangular baffle is 220 mm wide and vertical; the original tapered cabinet is approximately 220 mm wide at the base / 180 mm at the top with a 6 degree lean. The changed width, edges and tilt change diffraction, baffle step and time alignment. The same crossover therefore does not guarantee the same tonal balance or crossover summation.

The port retains a 50 mm bore, 185 mm mouth-to-inlet axial length and R14 outlet flare. Its centre is at rear z55, versus approximately z307.5 in the original. The inlet has 71.152 mm axial clearance to the front wall (greater than its bore), and its bore edge is 20 mm above the floor. Keep that area unlined and clear of wires. Different wall loading and flare end effects can shift tuning. The original nominal tuning is about 37 Hz; a simplified straight-cylinder Helmholtz estimate using 343 m/s and 0.85r + 0.61r end corrections is 40.5 Hz. Neither is a prediction validated for this acrylic build. Measure impedance and near-field port output before adjusting length or claiming a tuning frequency.

## Nominal volume ledger, litres

| Item | Acrylic |
|---|---:|
| gross cavity and driver wells | 17.606772 |
| printed fittings and acrylic brace | 0.738963 |
| port duct air | 0.337939 |
| woofer estimate | 0.192103 |
| tweeter estimate | 0.103732 |
| crossover material estimate | 0.120000 |
| spacers | 0.001536 |
| wiring allowance | 0.002500 |
| hardware allowance | 0.010000 |
| nominal net | 16.100000 |

The production air solid deducts physical CAD fittings and brace, port duct air, estimated driver material, 0.120 L crossover material, spacers, wire and 0.010 L hardware. The crossover clearance envelope is not treated as solid material. Driver shapes are approximate displacement proxies, not exact manufacturer CAD.

The A1 net is calculated separately from its saved air solid: **16.091519 L**. It restores brace material removed by prototype seams/holes and additional receiver holes, deducts the four internal brace straps and a further 0.004 L prototype hardware allowance. Outer sheet splices are outside the cavity. Small seam/foam effects are nominally sealed by the specified gaskets. Hardware and electronics allowances remain estimates; actual installed net volume can vary by a few tenths of a litre. The many displayed digits describe CAD arithmetic, not physical measurement accuracy.

10 mm acrylic, braced at z250..260, differs in stiffness and damping from the original wood cabinet. The frame rails and single four-wall brace provide structural support but no panel-resonance, load or fatigue analysis has qualified the result. Do not remove the brace. The printed tiled prototype verifies fit and construction only; its seams, infill and polymer do not establish acrylic acoustic performance.

Apply porous lining in upper side/rear regions without obstructing the port or drivers. After assembling the actual acrylic cabinet, check air leaks, impedance/tuning, near-field bass, response through the crossover and panel vibration. Physical acoustic validation remains outstanding.
