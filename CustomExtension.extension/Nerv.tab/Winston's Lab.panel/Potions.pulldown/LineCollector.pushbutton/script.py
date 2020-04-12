import clr, xlsxwriter, re, threading
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
import System
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, FamilySymbol, Transaction, FailureHandlingOptions, CurveElement
from Autodesk.Revit.UI import TaskDialog
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms

__doc__ = 'Print the element id of lines with a specific line style name'

lines = FilteredElementCollector(doc).OfClass(CurveElement).ToElements()
# print(len(lines))
lineStyles = ''
for i in lines:
    style = i.LineStyle.Name
    if style == 'Invisible' or style == 'INVISIBLE 2':
        lineStyles += str(i.Id.IntegerValue) + ';'
print(lineStyles)




