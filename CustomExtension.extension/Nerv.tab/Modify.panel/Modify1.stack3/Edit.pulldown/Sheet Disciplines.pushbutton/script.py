from pyrevit.framework import List
from pyrevit import revit, DB, forms
import clr,re
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
     Color, BuiltInParameter, ViewSheet
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')


Discipline = ['Architecture', 'Electrical', 'Mechanical', 'Structural', 'ARCHITECTURAL']

subDiscipline = {
    'Architecture': ['Architecture', 'Landscape'],
    'Electrical': ['Electrical', 'Electronics'],
    'Mechanical': ['HVAC', 'Plumbing', 'Fire Protection'],
    'Structural': ['Structural'],
    'ARCHITECTURAL': ['ARCHITECTURAL'],
}

def FillDisciplineandSubDiscipline(doc, discipline, SubDiscipline):
    sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
    dis = forms.SelectFromList.show(discipline, button_name='Select Model Discipline', multiselect=False)
    subDisList = SubDiscipline[dis]
    subDis = forms.SelectFromList.show(subDisList, button_name='Select Model subDiscipline', multiselect=False)
    if dis and subDis:
        for i in sheets:
            try:
                i.LookupParameter('Discipline Group').Set(str(dis))
                i.LookupParameter('Discipline Sub-Group').Set(str(subDis))
                print('Success changing Discipline and SubDiscipline on Sheet' + i.LookupParameter('Sheet Number').AsString())
            except:
                print('Failed to change Discipline and SubDiscipline on Sheet' + i.LookupParameter('Sheet Number').AsString())

# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Modify Sheet Disciplines' \
          'WARNING: will force change Sheet Disciplines ' \
          'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Select Action Item
actionList = ['Fill Discipline and SubDiscipline Code']
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

# Transaction Start
t = Transaction(doc, 'Add PA prefix to Name')
t.Start()

if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False,
                yes=False,
                no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Fill Discipline and SubDiscipline Code' in sel_action:
        FillDisciplineandSubDiscipline(doc, Discipline, subDiscipline)
    else:
        pass
t.Commit()