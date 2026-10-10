"""Run using FreeCADCmd to validate the saved native document."""
from pathlib import Path
import json
import FreeCAD as App, Part
ROOT=Path(__file__).resolve().parents[1]
doc=App.openDocument(str(ROOT/'cad/speaker_assembly.FCStd'));checks=[]
for obj in doc.Objects:
    if hasattr(obj,'SourceSTEP'):
        expected=Part.read(str(ROOT/obj.SourceSTEP))
        checks.append({'name':obj.Name,'valid':obj.Shape.isValid(),'STEP_volume_matches':abs(obj.Shape.Volume-expected.Volume)<.01})
result={'all_pass':len(checks)==84 and all(c['valid'] and c['STEP_volume_matches'] for c in checks),'objects':checks,'version':App.Version()[:3]}
(ROOT/'validation/freecad_report.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert result['all_pass']
App.closeDocument(doc.Name)
