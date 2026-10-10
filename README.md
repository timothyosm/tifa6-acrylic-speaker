# Tifa 6 acrylic speaker enclosure

A rectangular, M3-assembled speaker enclosure with **whole 10 mm panels and a one-piece bass-reflex port**. This is an independent enclosure derivative using the original SB Acoustics Tifa 6 drivers and crossover.

**Cabinet:** 220 W x 380 H x 262.652 D mm. **Net volume:** approximately 16.1 L. **Port:** 50 mm bore x 185 mm long with a flared outlet. One passive speaker; no amplifier compartment.

![Whole panel outlines](renders/whole_panels.png)

## Download and print

**[Download the current build ZIP](https://github.com/timothyosm/tifa6-acrylic-speaker/releases/latest/download/tifa6-current-build.zip)** or browse [all current STL files](exports/current/stl/).

| What you want to make | Parts |
|---|---|
| Panel and port geometry check | Seven whole panels + one-piece port: 8 prints |
| Complete printed test enclosure | All 19 current STLs, one of each |
| Final acrylic enclosure | Laser-cut seven sheets; print the 12 fittings |

The complete set includes six outer panels, one window brace, eight corner-rail pieces, two woofer-adapter halves, one tweeter adapter and one continuous port. The rail/adapter splits are retained from the established design; this release gathers the files rather than redesigning them. Printer size is unrestricted for the current set. Print at **100% scale in millimetres**.

The panel/port-only set does not include the corner supports or driver seats. Use the full set for an assembled fit test. All structural joints use M3 screws and replaceable seals; no solvent-bonded panels or aluminium rail substitutions are used.

## Build instructions

1. Read [printing and laser cutting](docs/current/printing-and-cutting.md), then the [hardware list](docs/current/hardware.md).
2. Follow the [assembly instructions](docs/current/assembly-instructions.md). Install the brace before the front/driver assembly.
3. Use the [print manifest](exports/current/print-manifest.csv) and [fastener map](exports/current/fastener-map.csv) to check quantities and locations.
4. Review [verification and acoustic limits](docs/current/verification-and-acoustics.md).

Current hardware: **72 M3 screws, 60 inserts and four port nuts**, plus washers, four crossover spacers and binding-post hardware. The rear panel removes with its port and crossover attached for service.

## Files

- [Current STLs](exports/current/stl/) — whole panels, fittings and one-piece port
- [Current DXF/SVG laser profiles](exports/current/laser/) — identical panel outlines, nominal 10 mm stock, uncompensated kerf
- [Current STEP assembly](exports/current/step/assembly_with_components.step) — includes approximate purchased components
- [Calibration coupon](exports/calibration/) — confirm stock thickness, hole fit and kerf
- [Editable CAD source](cad/speaker_assembly.py), [parameters](cad/speaker_parameters.json), [current build packager](cad/package_current_build.py)
- [Current validation report](exports/current/verification.json)
- [Manufacturer source links](docs/source-register.md) — original drivers, crossover and acrylic fabrication guidance

All earlier STL variants are retained under [A1 mini](exports/a1_mini/), [original unrestricted set](exports/unrestricted/), [panel-only set](exports/whole_panels/) and [standalone port](exports/one_piece_port/). **Do not combine their manifests or print the older port halves in addition to the current port.** Root-level documents under `docs/`, the existing PDF drawings and the FreeCAD assembly are historical split-port/A1 references; use `docs/current/` for this release.

## Validation status

Current STLs pass connected/watertight geometry checks. Panel outlines match their laser profiles, and the port fits the rear panel and clears the checked component envelopes. Physical printing, assembly, sealing, strength and acoustic testing have not been performed. The printed prototype does not establish acrylic acoustic behaviour, and the changed flat baffle does not guarantee the original Tifa frequency response.

## Rebuild the exports

Use Python 3.12 with `pip install -r cad/requirements.txt`. Run these commands from the repository root:

```sh
python cad/speaker_assembly.py
python cad/inspect_geometry.py
python cad/verify_profiles.py
python cad/export_whole_panels.py
python cad/export_one_piece_port.py
python cad/package_current_build.py
```

The first command regenerates the base variants and replaces `exports/`, so run the subsequent exporters to restore the current set. `cad/render_views.py` and `cad/make_documentation.py` reproduce the historical base illustrations/drawings. The FreeCAD macro and validator also target those base variants. The current assembly STEP is produced by `package_current_build.py`.

Python/JSON is the parametric source. FCStd contains imported editable solids and a dimension sheet, not a sketch-based feature history. The fixed panel layout assumes 220 x 380 mm and 10 mm stock; dimensional changes require reviewing fits and joints.

## References

This is not an official SB Acoustics enclosure release. The driver specifications and crossover belong to their respective rights holders. Manufacturer PDFs are linked from the source register rather than redistributed here.
