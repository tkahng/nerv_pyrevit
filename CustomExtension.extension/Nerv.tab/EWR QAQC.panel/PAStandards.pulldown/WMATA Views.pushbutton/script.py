from pyrevit.framework import List
from pyrevit import revit, DB, forms
import clr,re
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
     Color, BuiltInParameter, View, Viewport, ViewSheet
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')

__doc__ = 'Rename view names according to WMATA standard.'

dict = {'ThreeD': '3D',
        'AreaPlan': 'AP',
        'CeilingPlan': 'CP',
        'DraftingView': 'DR',
        'Detail': 'DV',
        'Elevation': 'EL',
        'FloorPlan': 'FL',
        'Legend': 'LG',
        'Section': 'SC',
        'Schedule': 'SQ'}

excemption = ['DrawingSheet', 'Undefined', 'DrawingSheet', 'ProjectBrowser', 'Report','SystemBrowser', 'CostReport',
              'LoadsReport', 'PresureLossReport', 'ColumnSchedule', 'PanelSchedule', 'Walkthrough', 'Rendering',
              'Internal']
prefixList = ['3D', 'AP', 'BS', 'CP', 'CS', 'DL', 'DR', 'DS', 'DV', 'EL', 'EP', 'ES', 'FE', 'FP', 'IE', 'KL', 'LG',
               'LP', 'MT', 'NB', 'NO', 'ON', 'QP', 'RD', 'RO', 'RP', 'SC', 'SL', 'SP', 'SQ', 'VL', 'WT',
              'FU', 'SP', 'FL', 'IE', 'LG', 'MT', 'GN', 'LN', 'QP', 'RD', 'RF', 'RP', 'SC', 'SL', 'SP',
              'AC', 'AX', 'CM', 'CO', 'FA', 'GP', 'LI', 'LT', 'NS', 'PA', 'PP', 'RS', 'SS', 'TC', 'WD',
              'CC', 'CD', 'CN','FP', 'FS', 'HP', 'MD', 'MH', 'PI', 'PL', 'SI', 'SK', 'SQ', 'VL', 'WT'
              'CF', 'DP', 'FD', 'FR', 'GC', 'L', 'PP', 'RE', 'SF', 'ST', 'TB', 'WG', 'XB']

def UniqueName(proposedName, namesList):
    num = 1
    nameIteration = proposedName + ' ' + str(num)
    while num < 999:
        if not proposedName in namesList:
            return proposedName
            break
        elif not nameIteration in namesList:
            return nameIteration
            break
        else:
            num += 1
            nameIteration = proposedName + ' ' + str(num)
            continue

def RenameViews(doc, dict, excempt):
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    names = []
    for i in views:
        name = i.Name
        names.append(name)
    viewRegex03 = re.compile(r'^\w\w-(.*)')
    for i in views:
        name = i.Name
        type = i.ViewType
        if  viewRegex03.findall(name) == []:
            try:
                if "{" in name:
                    print('Failed ' + name)
                elif "COBie" in str(name):
                    print('Failed ' + name)
                elif len(re.split('-', name)) <= 2 and not str(type) in excempt and not 'Revision Schedule' in str(name):
                    proposedName = UniqueName(dict[str(type)] + '-' + str(name), names)
                    names.append(proposedName)
                    i.Name = proposedName
                    print(name + ' Changed to ' + proposedName)
                elif len(re.split('-', name)) > 2 and not str(type) in excempt and not 'Revision Schedule' in str(name):
                    first = re.split('-', name)[0]
                    proposedName = UniqueName(dict[str(type)] + str(name)[len(first):],names)
                    names.append(proposedName)
                    i.Name = proposedName
                    print(name + ' Changed to ' + proposedName)
            except:
                print('Failed ' + name)

def FillTitleonSheetParam(doc):

    sheetViewIds = []
    viewports = FilteredElementCollector(doc).OfClass(Viewport).ToElements()
    for i in viewports:
        sheetViewIds.append(str(i.ViewId.IntegerValue))
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    for i in views:
        name = i.Name
        id = str(i.Id.IntegerValue)
        if id in sheetViewIds:
            title = i.LookupParameter('Title on Sheet').AsString()
            print('Name: ' + name)
            print('Title: ' + title)
            if not title:
                i.LookupParameter('Title on Sheet').Set(name)
                print('Set: ' + name)


# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Select Action Item
actionList = ['Rename Views', 'Fill Title on Sheet Parameter']
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

# Transaction Start
t = Transaction(doc, 'Rename view names according to WMATA standard.')
t.Start()
if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False,
                yes=False,
                no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Fill Title on Sheet Parameter' in sel_action:
        FillTitleonSheetParam(doc)
    if 'Rename Views' in sel_action:
        RenameViews(doc, dict, excemption)
    else:
        pass
t.Commit()