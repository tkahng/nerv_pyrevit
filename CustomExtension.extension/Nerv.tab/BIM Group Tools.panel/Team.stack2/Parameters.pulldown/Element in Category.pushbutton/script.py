from pyrevit.framework import List
from pyrevit import revit, DB
import pprint
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, ExternalFileReference, \
	BuiltInParameter, NestedFamilyTypeReference, FamilyInstance, AnnotationSymbol, Element
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

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import *
from System.Collections.Generic import List


doc = __revit__.ActiveUIDocument.Document


allModel = DB.FilteredElementCollector(doc)\
            .WhereElementIsNotElementType()\
              .ToElements()

print(len(allModel))
allLst = []
for instance in allModel:
    cate = instance.Category
    if str(cate) != 'None':
        a = str(cate.Name)
        if instance.GetType() != AnnotationSymbol and str(cate.CategoryType) == 'Model' and \
                str(cate.Name) != 'Detail Items' and cate.AllowsBoundParameters == True and a != 'Sheets'\
                and a != 'Materials' and a != 'RVT Links' and a != 'Areas' and a != 'Project Information':

            workset = instance.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
            combine = str(cate.Name) + ':' + str(workset)
            if not combine in allLst:
                allLst.append(combine)
                print(combine)
# print(allLst)