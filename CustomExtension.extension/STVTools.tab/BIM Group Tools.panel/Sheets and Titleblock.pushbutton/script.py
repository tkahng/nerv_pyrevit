from pyrevit.framework import List
from pyrevit import revit, DB
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, ExternalFileReference
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import *
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selection = [doc.GetElement(id)
            for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]

__doc__ = 'Select the shared point of the model '\
          'This is helpful check project info'

# containment -----------------------------------
tab = '		'
ttBlock = []
titleNumber = []
titleFamily = []
titleType = []
titleKeyPlan = []
titleNorthArrow = []
titleKeyType = []
titleBlock = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).ToElements()
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
for t in titleBlock:
	tNumber = t.LookupParameter('Sheet Number')
	if tNumber != None:
		number = tNumber.AsString()
		ttBlock.append(t)
for b in ttBlock:
	tNumber = b.LookupParameter('Sheet Number').AsString()
	tFamily = b.Symbol.FamilyName
	tType = b.Symbol.ToString()

	tKeyPlan = b.LookupParameter('Key Plan')
	if tKeyPlan == None:
		tKplan = 'No Key Plan'
	else:
		tKplan = 'Key Plan : ' + tKeyPlan.AsValueString()

	tNortharrow = b.LookupParameter('North Arrow')
	if tNortharrow == None:
		tNarrow = 'No North Arrow'
	else:
		tNarrow = 'North Arrow : ' + tKeyPlan.AsValueString()
	'''
	tKeytype = b.LookupParameter('Key Plan Type<Generic Annotations>')
	if tKeytype == None:
		tKtype = 'No Key Plan'
	else:
		tKtype = tKeyPlan.AsString()
	'''
	titleNumber.append(tNumber)
	titleFamily.append(tFamily)
	titleType.append(tType)
	titleKeyPlan.append(tKplan)
	titleNorthArrow.append(tNarrow)
	# titleKeyType.append(tKtype)

count = 0
print('-------------------------------------------')
for sheet in sheets:
	sNumber = sheet.LookupParameter('Sheet Number').AsString()
	sSubmittal = sheet.LookupParameter('Submittal').AsString()
	print(sNumber + tab + sSubmittal + tab + titleNumber[count] + tab + titleFamily[count] + tab + titleType[count] + tab +
		  titleKeyPlan[count] + tab + titleNorthArrow[count])
	count += 1




