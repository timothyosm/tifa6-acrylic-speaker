# Verification and acoustic limits

The current build is 220 W x 380 H x 262.652 D mm, excluding driver/port/screw protrusions. It retains the original SB16PFCR25-4 woofer, SB26ST-C000-5 tweeter and passive Tifa 6 crossover. Driver centres are z160 and z324.1 (164.1 mm spacing), with printed seats at 3.6 and 3.0 mm depth.

The cabinet was solved for 16.1 litres with the previous port coupling. Removing that collar slightly increases volume; the current saved air solid and exact nominal result are in `exports/current/verification.json`. It remains approximately 16.1 litres. Driver, crossover, wire and metal hardware displacement are estimates, so this is not a measured finished-cabinet volume.

The one-piece port preserves 50 mm bore, 185 mm axial length, R14 flare, 72.5 mm spigot and four M3 holes on 88 mm PCD. It fits the 73 mm rear-panel opening and retains a 71.15 mm inlet approach to the front wall. Its centre is z55. Its mounting uses four M3 x20 screws; no coupling fasteners remain.

The current meshes are valid connected, watertight solids. Their unchanged panel/fitting geometry inherits the recorded interference, screw clearance, insert engagement and laser-profile checks. The new port is checked against the saved assembly and approximate driver/crossover envelopes. The current STEP assembly contains the one-piece port. The existing FreeCAD document, older PDF drawing pack and base geometry reports describe the earlier split-port variants and are retained as historical references.

The flat 220 mm-wide baffle differs from the original tapered 180-220 mm, 6-degree tilted baffle. Diffraction, time alignment and crossover summation can differ; acrylic also differs from the original wood cabinet in stiffness and damping. Retain the specified crossover values and polarity, but do not assume identical sound. Original nominal tuning is about 37 Hz; actual tuning of this cabinet requires measurement.

Still outstanding: physical printing, laser cutting, fit, hand/tool access, seal compression, insert retention, leakage, structural behaviour and acoustic measurements. A printed test cabinet verifies construction and geometry; it does not establish acrylic acoustic performance. Do not remove the four-wall brace.
