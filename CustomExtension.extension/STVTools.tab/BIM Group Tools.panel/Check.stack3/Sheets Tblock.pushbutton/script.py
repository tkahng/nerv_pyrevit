from pyrevit.framework import List
from pyrevit import revit, DB
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, ExternalFileReference, \
	BuiltInParameter, NestedFamilyTypeReference, FamilyType
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
# Collection Lists
tab = '		'
ttBlock = []
titleNumber = []
titleFamily = []
titleType = []
titleKeyPlan = []
titleNorthArrow = []
titleKeyType = []
kt = 0
# Title Block and Sheets Collector
titleBlock = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).ToElements()
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()


# Sheet Number Filter
for t in titleBlock:
	tNumber = t.LookupParameter('Sheet Number')
	if tNumber != None:
		number = tNumber.AsString()
		ttBlock.append(t)
# Sheet Collector
for b in ttBlock:
	# Sheet Number Collector
	tNumber = b.LookupParameter('Sheet Number').AsString()
	# Family Name Collector
	tFamily = b.Symbol.FamilyName
	tnestedFamily = b.GetExternalFileReference()
	for i in tnestedFamily:
		print(i.Count)
	# Family Type Collector
	tType =b.Symbol.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
	# KeyPlan Collector
	tKeyPlan = b.LookupParameter('Key Plan')
	if tKeyPlan == None:
		tKplan = 'Without Key Plan'
	else:
		tKplan = 'Key Plan : ' + tKeyPlan.AsValueString()
# North Arrow Collector
	tNortharrow = b.LookupParameter('North Arrow')
	if tNortharrow == None:
		tNarrow = 'Without North Arrow'
	else:
		tNarrow = 'North Arrow : ' + tKeyPlan.AsValueString()

	tKeytype = b.LookupParameter('Key Plan Type')

	if tKeytype == None:
		tKtype = 'Without Key Plan Type'
	else:
		tKtype = 'Key Plan Type: ' + tKeyPlan.AsString()

	titleNumber.append(tNumber)
	titleFamily.append(tFamily)
	titleType.append(tType)
	titleKeyPlan.append(tKplan)
	titleNorthArrow.append(tNarrow)
	titleKeyType.append(tKtype)
	kt += 1


count = 0
print('Here are all the sheet Info: ')
print('-------------------------------------------')
print(len(ttBlock),
len(titleNumber),
len(titleFamily),
len(titleType),
len(titleKeyPlan),
len(titleNorthArrow),
len(titleKeyType))
print(len(sheets))
for sheet in sheets:
	sNumber = sheet.LookupParameter('Sheet Number').AsString()
	sSubmittal = sheet.LookupParameter('Submittal').AsString()
	if sNumber == None:
		pass
	if sSubmittal != None:
		print(sNumber + tab + sSubmittal + tab + titleNumber[count] + tab + titleFamily[count] + tab +
			  titleType[count] + tab + titleKeyPlan[count] + tab + titleKeyType[count] + tab + titleNorthArrow[count])
		count += 1




