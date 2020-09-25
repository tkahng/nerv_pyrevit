from pyrevit.framework import List
from pyrevit import revit, DB, forms
import clr,re,random
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
    CurveElement, Color, FilledRegion, BuiltInParameter
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application

__doc__ = 'Delete Excess Filled Regions and/or Add PA - to Filled Regions'

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')
# Define the prefix we want to track and add
prefix = 'PA - '

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

def SetFilledRegion(doc, sourceFilledRegion, DestinationFilledRegion):
    fills = FilteredElementCollector(doc).OfClass(FilledRegion).ToElements()
    for i in fills:
        if i.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsElementId().ToString() == sourceFilledRegion:
            i.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).Set(DestinationFilledRegion)
            # print(sourceLineStyle.Name + ' is being changed to ' + DestinationLineStyle.Name)

def CollectFilledRegionFromDoc(doc):
    fills = FilteredElementCollector(doc).OfClass(FilledRegion).ToElements()
    # print(len(lines))
    filledRegions = []
    for i in fills:
        name = i.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsElementId().ToString()
        if not name in filledRegions:
            filledRegions.append(name)
    return filledRegions

def DeleteExcessFilledRegions(doc, list):
    fills = FilteredElementCollector(doc).OfClass(FilledRegionType).ToElements()
    for i in fills:
        name = i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        id  = i.Id.ToString()
        if not id in list and name[0] != '<' and name[0:5] != prefix and i.Id.IntegerValue > 0:
            #try:
            print('Deleting Filled Region Style ' + name)
            doc.Delete(i.Id)
            # except:
                # print('Error: Failed to Delete ' + name + ' ' + i.Id.ToString())

def ConsolidateRegion(doc):
    styles = FilteredElementCollector(doc).OfClass(FilledRegionType).ToElements()
    _dict = {}
    paramList = []
    ids = []
    names = []
    # Unique Graphic Style Collector
    for i in styles:
        try:
            patternId = i.FillPatternId
        except:
            patternId = "Solid"
        lineWeight = i.LineWeight
        try:
            back = i.Background
        except:
            back = "None"
        color = str(i.Color.Red) +str(i.Color.Green) + str(i.Color.Blue)
        name = i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        id = i.Id
        unique_param = str(patternId.IntegerValue) + str(lineWeight) + str(back) + color
        if not unique_param in paramList:
            paramList.append(unique_param)
            ids.append(id)
            _dict[str(unique_param)] = id
    for i in styles:
        names.append(i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString().lower())
    # Non-Standard Line Changer
    instances = FilteredElementCollector(doc).OfClass(FilledRegion).ToElements()
    for i in instances:
        name = i.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsElementId()
        filledType = doc.GetElement(name)
        try:
            patternName = filledType.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        except:
            patternName = ''
        try:
            uniqueParam = str(filledType.FillPatternId.IntegerValue) + str(filledType.LineWeight) + \
                          str(filledType.Background) + str(filledType.Color.Red) + str(filledType.Color.Green) + \
                          str(filledType.Color.Blue)
        except:
            uniqueParam = 0
        if uniqueParam in paramList and not name in ids and patternName[0:len(prefix)] != prefix:
            newName = UniqueName(prefix.lower + ' - ' + patternName, names)
            i.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).Set("PA" + newName[2:])
            names.append(newName)
            print(filledType.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString() + ' changed to ' +
                  doc.GetElement(_dict[str(uniqueParam)]).get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString())

def AddPAtoRegion(doc):
    styles = FilteredElementCollector(doc).OfClass(FilledRegionType).ToElements()
    names = []
    dict ={}
    for i in styles:
        names.append(i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString().lower())
    print(names)
    for i in styles:
        name = i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        if name[0:len(prefix)] != prefix and not '.dwg' in name and i.Id.IntegerValue > 0:
            #try:
            newName = UniqueName(prefix.lower()+name.lower(), names)
            print("%" + newName)
            destination = i.Duplicate("PA" + newName[2:])
            SetFilledRegion(doc, str(i.Id.IntegerValue), destination.Id)
            doc.Delete(i.Id)
            # print('Renamed ' + name + ' to ' + prefix + name)
            names.append(newName)
            #except:
                #print('Failed to Delete ' + name + i.Id.ToString())
        elif '.dwg' in name:
            try:
                try:
                    patternIdName = str(doc.GetElement(i.FillPatternId).Name).replace('.dwg', ' ')
                except:
                    patternIdName = str(doc.GetElement(i.FillPatternId).Name)
            except:
                patternIdName ='Pattern'
            proposedName = prefix + patternIdName + ' ' + str(i.Background)
            num = 0
            nameIteration = proposedName + ' - ' + str(num)
            while num < 999:
                if not proposedName in names:
                    destination = i.Duplicate(proposedName)
                    names.append(proposedName)
                    break
                elif not nameIteration in names:
                    destination = i.Duplicate(nameIteration)
                    names.append(nameIteration)
                    break
                else:
                    num += 1
                    nameIteration = proposedName + ' - ' + str(num)
                    continue
            try:
                SetFilledRegion(doc, str(i.Id.IntegerValue), destination.Id)
                doc.Delete(i.Id)
            except:
                print('Fail' + name)
            # print('Renamed ' + name + ' to ' + destination.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString())
            names.append(proposedName)

# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Select Action Item
actionList = ['Delete Excess Filled Regions',
              'Add PA - to Filled Regions',]
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

# Transaction Start
t = Transaction(doc, 'Add PA prefix to Name')
t.Start()
if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False,
                yes=False,
                no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Delete Excess Filled Regions' in sel_action:
        list = CollectFilledRegionFromDoc(doc)
        # try:
        DeleteExcessFilledRegions(doc, list)
        # except:
            # print("Fail 1")
    if 'Add PA - to Filled Regions' in sel_action:
        list = CollectFilledRegionFromDoc(doc)
        # try:
        ConsolidateRegion(doc)
        DeleteExcessFilledRegions(doc, list)
        AddPAtoRegion(doc)
        # except:
            # print("Fail 2")
    else:
        pass
t.Commit()