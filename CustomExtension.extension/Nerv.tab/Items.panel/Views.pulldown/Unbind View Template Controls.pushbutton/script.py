
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
from System.Collections.Generic import List
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory, RevitLinkInstance, UV, XYZ,SpatialElementBoundaryOptions, CurveArray,ElementId, View

from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
views = FilteredElementCollector(doc).OfClass(View).ToElements()

__doc__ = 'Unbinde specific View Template Controls'

templates = {}
rawParam = {}

for v in views:
	if str(v.ViewTemplateId) != "-1":
		templates[doc.GetElement(v.ViewTemplateId).Name] = doc.GetElement(v.ViewTemplateId)

selectedTemplates = forms.SelectFromList.show(templates.keys(), button_name='Select Item', multiselect=True)

for c in selectedTemplates:
	for v in templates[c].Parameters:
		rawParam[v.Definition.Name] = v.Id
	break

selectedPrarm = forms.SelectFromList.show(rawParam.keys(), button_name='Select Item', multiselect=True)


t = Transaction(doc, 'Change Template')
t.Start()
for c in selectedTemplates:
	para = List[ElementId]()
	for v in templates[c].Parameters:
		if v.Definition.Name in selectedPrarm:
			para.Add(v.Id)
	templates[c].SetNonControlledTemplateParameterIds(para)
selection = Selection.get_selected_elements(doc)
t.Commit()

