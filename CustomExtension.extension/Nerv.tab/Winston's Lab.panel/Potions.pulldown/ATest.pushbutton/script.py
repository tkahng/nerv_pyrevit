
import sys, clr
import ConfigParser
from os.path import expanduser
# Set system path
home = expanduser("~")
cfgfile = open(home + "\\STVTools.ini", 'r')
config = ConfigParser.ConfigParser()
config.read(home + "\\STVTools.ini")
# Master Path
syspath1 = config.get('SysDir','MasterPackage')
sys.path.append(syspath1)
# Built Path
syspath2 = config.get('SysDir','SecondaryPackage')
sys.path.append(syspath2)
import Selection
clr.AddReference('System')
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory,\
    RevitLinkInstance, UV, XYZ, SpatialElementBoundaryOptions, CurveArray, ElementId, View, RevitLinkType, WorksetTable,\
    Workset, FilteredWorksetCollector, WorksetKind, RevitLinkType, RevitLinkInstance

from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


worksetDic = {
'*LINKED STRUCT-FQ19144N-BL001':'*LINKED T06-STRUCT-NBusGarage-r20',
'*LINKED HSSTRU-FQ19144N-BL001':'*LINKED T06-HSSTRU-NBusGarage-r20',
'*LINKED ARCH-FQ19144N-BL001':'*LINKED T06-ARCH-NBusGarage-r20',
'*LINKED MECH-FQ19144N-BL001':'*LINKED T06-MECH-NBusGarage-r20',
'*LINKED ELECT-FQ19144N-BL001':'*LINKED T06-ELECT-NBusGarage-r20',
'*LINKED SIGNAGE-FQ19144N-BL001':'*LINKED T06-SIGNAGE-NBusGarage-r20',
'*LINKED FOUNDA-FQ19144N-BL001':'*LINKED T06-FOUNDA-NBusGarage-r20',
'*LINKED INDU-FQ19144N-BL001':'*LINKED T06-INDU-NBusGarage-r20',
'*LINKED INDUPLUM-FQ19144N-BL001':'*LINKED T06-INDUPLUM-NBusGarage-r20',
'*LINKED SURVEY-FQ19144N-BL001':'*LINKED T06-SURVEY-NBusGarage-r20',
'*LINKED HSARCH-FQ19144N-BL001':'*LINKED T06-HSARCH-NBusGarage-r20',
'*LINKED ESOLAR-FQ19144N-BL001':'*LINKED T06-ESOLAR-NBusGarage-r20'}

worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
#print("1")
t = Transaction(doc, 'Change Name')
t.Start()

for workset in worksets:
    if workset.Name in worksetDic.keys():
        WorksetTable.RenameWorkset(doc, workset.Id, worksetDic[workset.Name])

t.Commit()
'''
links = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
for l in links:
    modelPath = 
    print(l.LookupParameter('Workset').AsValueString())
    l.LoadFrom(ModelPath, WorksetConfiguration)
    #print(l.Name.split(":")[0])
    #print(l.GetType().ToString())

t.Commit()


for i in families:
    try:
        proposedName = i.Family.Name.replace(" - ", "-")
        if i.Family.Name != proposedName:
            i.Family.Name = proposedName
    except:
        print("Failure")


'''