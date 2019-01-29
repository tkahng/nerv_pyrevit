from pyrevit.framework import List
from pyrevit import revit, DB, forms
import clr, re
from fractions import Fraction
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')
# Collect Save location and Rvt Files
prefix  = 'PA - '
'''
def SplitString(name):
    pieces = re.split(name)
    if '.dwg' is in name:
        
    if len(pieces) >= 2:
        out = pieces[len(pieces)]
'''
# TODO Fix this function
def AddPrefixtoAnnotation(doc):
        levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
        discipline = str(doc.Title)[0]
        for i in levels:
            if i.Name[0:4] != discipline + ' - ':
                print('Changing '+ i.Name + ' to '+ discipline + ' - ' + i.Name )
                i.Name = discipline + ' - ' + i.Name
            else:
                print('Unable to change ' + i.Name)

# TODO Fix this function
def AddPrefixtoLines(doc):
    levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
    for i in levels:
        height = FeettoInch(i.Elevation)
        if not str(height) in i.Name:
            print('Changing ' + i.Name + ' to ' + i.Name + ' ' + height)
            i.Name = i.Name + ' ' + str(height)
        else:
            print('Unable to change ' + i.Name)

# TODO Fix this function
def AddPrefixtoFilledRegion(doc):
    levels = FilteredElementCollector(doc).OfClass(FilledRegionType).ToElements()
    for i in levels:
        height = FeettoInch(i.Elevation)
        if not str(height) in i.Name:
            print('Changing ' + i.Name + ' to ' + i.Name + ' ' + height)
            i.Name = i.Name + ' ' + str(height)
        else:
            print('Unable to change ' + i.Name)

# TODO Fix this Function
def AddPrefixtoTextStyle(doc):
    pass
# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Open projects and resave in a specific location'\
            'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application


# Transaction
actionList = ['Add PA - to Annotation Symbol', 'Add PA - to Line Styles', 'Add PA - to Filled Region']
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

t = Transaction(doc, 'Change Level Name')
t.Start()
if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Add PA - to Annotation Symbol' in sel_action:
        AddPrefixtoAnnotation(doc)
    if 'Add PA - to Line Styles' in sel_action:
        AddPrefixtoLines(doc)
    if 'Add PA - to Line Styles' in sel_action:
        AddPrefixtoFilledRegion(doc)
t.Commit()