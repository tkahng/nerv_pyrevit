from pyrevit.framework import List
from pyrevit import revit, DB, forms
import clr
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
    CurveElement, Color, FilledRegion, BuiltInParameter
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')
# Define the prefix we want to track and add
prefix = 'PA - '

def SetFilledRegion(doc, sourceFilledRegion, DestinationFilledRegion):
    fills = FilteredElementCollector(doc).OfClass(FilledRegion).ToElements()
    for i in fills:
        if i.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).AsElementId().ToString() == sourceFilledRegion:
            i.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM) = DestinationFilledRegion

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
            try:
                print('Deleting Filled Region Style ' + name)
                doc.Delete(i.Id)
            except:
                print('Failed to Delete ' + name)

def AddPrefixtoLines(doc):
    Styles = FilteredElementCollector(doc).OfClass(FilledRegionType).ToElements()
    _dict = {}
    paramList = []
    out = []
    # Unique Graphic Style Collector
    for i in Styles:
        lineColor = int(i.LineColor.Red + i.LineColor.Green + i.LineColor.Blue)
        weight = i.GetLineWeight(GraphicsStyleType.Projection).ToString()
        pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
        if pattern is None:
            patternName = 'Solid'
        else:
            patternName = pattern.Name
        # unique parameter of line weight + line pattern as a parameter indicator
        uniqueParam = weight + patternName
        if not uniqueParam in paramList and lineColor == 0:
            if i.Name[0:len(prefix)] == prefix or i.Id.IntegerValue < 0:
                # Create standard line style dictionary
                line_dict[uniqueParam] = i
                paramList.append(uniqueParam)

    # Non-Standard Line Changer
    for i in lineStyles:
        if not i.Name[0:len(prefix)] == prefix and not i.Id.IntegerValue < 0:
            weight = i.GetLineWeight(GraphicsStyleType.Projection).ToString()
            pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
            if pattern is None:
                patternName = 'Solid'
            else:
                patternName = pattern.Name
            uniqueParam = weight + patternName
            # Try changing it to an existing line style in dictionary
            try:
                SetLineStyle(doc, i, line_dict[uniqueParam])
                print('Changed ' + i.Name + ' to ' + line_dict[uniqueParam].Name)
                doc.Delete(i.Id)
            # Create a new, properly named Line Style
            except:
                categories = doc.Settings.Categories
                lineCat = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
                newName = prefix + 'Pen # ' + str(weight) + ' ' + str(patternName)
                newLineStyleCat = categories.NewSubcategory(lineCat, newName)
                doc.Regenerate()
                newLineStyleCat.SetLineWeight(int(weight), GraphicsStyleType.Projection)
                newLineStyleCat.LineColor = Color(0x00, 0x00, 0x00);
                try:
                    newLineStyleCat.SetLinePatternId(pattern.Id, GraphicsStyleType.Projection)
                except:
                    pass
                # Add new Line style to dictionary
                line_dict[uniqueParam] = newLineStyleCat
                print('Renamed ' + i.Name + ' to ' '\'' +
                      newName + '\'')
                SetLineStyle(doc, i, newLineStyleCat)
                doc.Delete(i.Id)


# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'WARNING: will delete line styles ' \
          'Please do not use lightly'
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
        DeleteExcessFilledRegions(doc, list)
    if 'Add PA - to Filled Regions' in sel_action:
        list = CollectFilledRegionFromDoc(doc)
        AddPrefixtoLines(doc)
    else:
        pass
t.Commit()