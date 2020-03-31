from pyrevit.framework import List
from pyrevit import revit, DB, forms
import clr, re
from fractions import Fraction
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
    CurveElement, Color, DimensionType, BuiltInParameter, Dimension, DimensionType, FormatOptions, DisplayUnitType, \
    UnitSymbolType
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')

__doc__ = 'Reset Dimension rounding.'

# Collect Save location and Rvt Files
prefix  = 'PA - '

def SetDimensionStyle(doc, source, destination):
    elements = FilteredElementCollector(doc).OfClass(Dimension).ToElements()
    for i in elements:
        if i.LookupParameter('Type').AsValueString() == source:
            i.LookupParameter('Type').Set(destination.Id)

def SplitString(name):
    pieces = re.split(name)
    if '.dwg' in name:
        if len(pieces) >= 2:
            out = pieces[len(pieces)]

# TODO Fix this Function
def SetDimensiontoOneEigth(doc):
    dimension = FilteredElementCollector(doc).OfClass(DimensionType).ToElements()
    format = FormatOptions(DisplayUnitType.DUT_FEET_FRACTIONAL_INCHES, 0.125/12)
    for i in dimension:
        try:
            method = (i.GetUnitsFormatOptions().Accuracy * 12)
            if method > 0.125:
                i.SetUnitsFormatOptions(format)
                print(i.LookupParameter('Type Name').AsString() + ' Reset to 1/8 inch rounding')
        except:
            pass


# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


uiapp = UIApplication(doc.Application)
application = uiapp.Application


# Select Action Item
actionList = ['Set Dimension to 1/8" Accuracy or less']
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

# Transaction Start
t = Transaction(doc, 'Set Dimension to 1/8" Accuracy or less')
t.Start()

if sel_action == None:

    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Set Dimension to 1/8" Accuracy or less' in sel_action:
        SetDimensiontoOneEigth(doc)
    else:
        pass

t.Commit()