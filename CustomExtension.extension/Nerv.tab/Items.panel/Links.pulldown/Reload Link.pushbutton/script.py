from pyrevit.framework import List
from pyrevit import revit, DB, forms
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, ExternalFileReference, RevitLinkType, Transaction, \
	ModelPathUtils,WorksetConfiguration, WorksetConfigurationOption, BuiltInParameter
from System.Collections.Generic import List
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selection = [doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]

__doc__ = 'Reload Model Link or reload from other place.'

# Pick the Link you want to relink
allLinkObj = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
wsOpt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
names = []
LinkObj = []
for i in allLinkObj:
	names.append(i.Parameter[BuiltInParameter.SYMBOL_NAME_PARAM].AsString())
sel_model = forms.SelectFromList.show(names, button_name='Select Item', multiselect=True)
for i in allLinkObj:
	if i.Parameter[BuiltInParameter.SYMBOL_NAME_PARAM].AsString() in sel_model:
		LinkObj.append(i)

# t = Transaction(doc, 'Reload Models From')
# Reload Transaction
# t.Start()
for i in LinkObj:
	name = i.Parameter[BuiltInParameter.SYMBOL_NAME_PARAM].AsString()
	gate = forms.alert('Please pick new location for ' + name, title = 'Reload From', yes = True, no = True)
	print('Please select file: ' + name)
	if gate:
		filePath = forms.pick_file(file_ext='rvt', multi_file=False, unc_paths=False)
		modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(filePath)
		i.LoadFrom(modelPath, wsOpt)
	else:
		break
# t.Commit()




