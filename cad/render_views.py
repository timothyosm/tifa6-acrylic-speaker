from speaker_assembly import *
import vtk

def actor(s,color,opacity=1):
    verts,faces=s.tessellate(.18,.14)
    points=vtk.vtkPoints()
    for v in verts:points.InsertNextPoint(v.x,v.y,v.z)
    cells=vtk.vtkCellArray()
    for f in faces:
        cells.InsertNextCell(3)
        for i in f:cells.InsertCellPoint(i)
    pd=vtk.vtkPolyData();pd.SetPoints(points);pd.SetPolys(cells)
    norm=vtk.vtkPolyDataNormals();norm.SetInputData(pd);norm.SetFeatureAngle(45);norm.Update()
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(norm.GetOutputPort())
    ac=vtk.vtkActor();ac.SetMapper(mapper);ac.GetProperty().SetColor(*color);ac.GetProperty().SetOpacity(opacity);ac.GetProperty().SetSpecular(.18);ac.GetProperty().SetSpecularPower(22)
    return ac

def render(items,name,camera,focus=(0,160,180),title='',subtitle=''):
    r=vtk.vtkRenderer();r.SetBackground(.93,.94,.95)
    for item in items:r.AddActor(actor(*item))
    cam=r.GetActiveCamera();cam.SetPosition(*camera);cam.SetFocalPoint(*focus);cam.SetViewUp(0,0,1);cam.ParallelProjectionOn();cam.SetParallelScale(330 if name!='exploded' else 500)
    for pos,intensity in [((200,-400,900),.9),((-500,-200,400),.55),((200,600,500),.7)]:
        light=vtk.vtkLight();light.SetPosition(*pos);light.SetFocalPoint(*focus);light.SetIntensity(intensity);r.AddLight(light)
    text=vtk.vtkTextActor();text.SetInput(title+'\n'+subtitle);text.GetTextProperty().SetFontSize(24);text.GetTextProperty().SetColor(.15,.18,.21);text.SetPosition(40,1020);r.AddViewProp(text)
    r.ResetCameraClippingRange()
    win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1600,1120);win.AddRenderer(r);win.Render()
    capture=vtk.vtkWindowToImageFilter();capture.SetInput(win);capture.Update()
    writer=vtk.vtkPNGWriter();writer.SetFileName(str(ROOT/'renders'/f'{name}.png'));writer.SetInputConnection(capture.GetOutputPort());writer.Write();win.Finalize()

meta=json.loads((ROOT/'validation/geometry_report.json').read_text())
W,D,H=meta['dimensions_mm'];dark=(.12,.15,.17);acrylic=(.38,.68,.74);orange=(.9,.49,.16)
def load_variant(v):
    path=ROOT/'exports'/v/'step'
    return {n:cq.importers.importStep(str(path/(n+'.step'))).val() for n in meta['variants'][v]['assembly_parts']}
parts=load_variant('unrestricted');proto=load_variant('a1_mini')
path=ROOT/'exports/unrestricted/step'
refs={n:cq.importers.importStep(str(path/('reference_'+n+'.step'))).val() for n in ['woofer','tweeter','crossover']}
items=[(s,acrylic,.3) if n in meta['panel_profiles'] else (s,dark,1) for n,s in parts.items()]
render(items+[(refs[n],dark,1) for n in ['woofer','tweeter']],'assembled',(650,-1050,520),focus=(0,130,190),title='10 MM ACRYLIC / M3 ASSEMBLY',subtitle=f'220 x {D:.1f} x 380 mm | 16.1 L nominal | Clear material shown for inspection')
render(items+[(refs['crossover'],(.5,.57,.6),1)],'rear',(-650,1000,530),focus=(0,130,190),title='REMOVABLE REAR PANEL',subtitle='Port and crossover come away with the rear panel; undo eight rail screws')
exploded=[]
for n,s in parts.items():
    move=(0,0,0)
    if n=='front' or 'adapter' in n:move=(0,-130,0)
    elif n=='rear' or n.startswith('port_'):move=(0,120,0)
    elif n=='left':move=(-105,0,0)
    elif n=='right':move=(105,0,0)
    elif n=='top':move=(0,0,100)
    elif n=='bottom':move=(0,0,-90)
    elif n=='brace':move=(0,0,35)
    exploded.append((s.translate(move),acrylic if n in meta['panel_profiles'] else dark,.7 if n in meta['panel_profiles'] else 1))
render(exploded,'exploded',(800,-1100,600),focus=(0,140,190),title='UNRESTRICTED / LASER-CUT BUILD',subtitle='Six outer sheets + one window brace | Eight rails + three adapter pieces + two port pieces')
view=[]
for n,s in proto.items():
    view.append((s,orange if n.startswith('splice_') else acrylic if n in meta['prototype_tiles'] else dark,1))
render(view,'a1_prototype',(650,-1050,520),focus=(0,130,190),title='A1 MINI / SAME ASSEMBLED PANEL GEOMETRY',subtitle='32 sheet tiles | 13 fittings | 15 temporary joining pieces shown in orange')
section=[]
for n,s in {**parts,**refs}.items():
    cut=s.intersect(box(0,-10,-10,200,400,450))
    if cut.Volume()>.01:section.append((cut,acrylic if n in meta['panel_profiles'] else dark,1))
render(section,'sectional',(-1000,-300,530),focus=(0,130,190),title='INTERNAL FIT / NO AMPLIFIER',subtitle='Printed driver seats | Four-wall window brace | 50 mm bore, 185 mm port')
print('Rendered acrylic production and A1 prototype assemblies')
