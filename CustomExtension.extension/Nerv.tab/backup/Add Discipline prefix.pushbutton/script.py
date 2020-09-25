from pyrevit import revit, DB, forms
import clr
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level
from Autodesk.Revit.UI import UIApplication
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')
# Collect Save location and Rvt Files

__doc__ = 'Add Discipline code to Level.'

def AddDisciplinetoLevel(doc):
        levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
        discipline = str(doc.Title)[0]
        for i in levels:
            if i.Name[0:4] != discipline + ' - ' and i.Name[0:2] != discipline + '-':
                print('Changing '+ i.Name + ' to '+ discipline + ' - ' + i.Name )
                i.Name = discipline + ' - ' + i.Name
            else:
                print('Unable to change ' + i.Name)

def AddLevelNumtoLevel(doc):
    levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
    for i in levels:
        height = FeettoInch(i.Elevation)
        if not str(height) in i.Name:
            print('Changing ' + i.Name + ' to ' + i.Name + ' ' + height)
            i.Name = i.Name + ' ' + str(height)
        else:
            print('Unable to change ' + i.Name)

def FeettoInch(number):
    feet = int(number)
    inch = (number - feet) * 12
    inchInt = int(inch)
    result = str(feet) + '\' ' + str(inchInt) + '\"'
    return result

# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Transaction
actionList = ['Add Discipline code to Level']
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item',
                                        multiselect=False)
print(sel_action)
t = Transaction(doc, 'Change Level Name')
t.Start()
if sel_action == 'Add Discipline code to Level':
    AddDisciplinetoLevel(doc)
elif sel_action == 'Add Height to Level':
    AddLevelNumtoLevel(doc)
elif sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)
t.Commit()