from pyrevit.framework import List
from pyrevit import revit, DB, forms
import clr
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
    CurveElement, Color, BuiltInParameter
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')
# Define the prefix we want to track and add
prefix = 'PA - '

def SetLineStyle(doc, sourceLineStyle, DestinationLineStyle):
    lines = FilteredElementCollector(doc).OfClass(CurveElement).ToElements()
    for i in lines:
        if i.LineStyle.Name == sourceLineStyle.Name:
            i.LineStyle = DestinationLineStyle.GetGraphicsStyle(GraphicsStyleType.Projection)
            # print(sourceLineStyle.Name + ' is being changed to ' + DestinationLineStyle.Name)


def CollectLineStylefromLine(doc):
    lines = FilteredElementCollector(doc).OfClass(CurveElement).ToElements()
    lineStyles = []
    for i in lines:
        if not i.LineStyle.Name in lineStyles:
            lineStyles.append(i.LineStyle.Name)
    return lineStyles


def DeleteExcessLineStyles(doc, list):
    lineStyle = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
    for i in lineStyle:
        if not i.Name in list and i.Name[0] != '<' and i.Name[0:5] != prefix and i.Id.IntegerValue > 0:
            try:
                print('Deleting Line Style ' + i.Name)
                doc.Delete(i.Id)
            except:
                print('Failed to Delete ' + i.Name)


def AddPrefixtoLines(doc):
    lineStyles = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
    line_dict = {}
    paramList = []
    out = []
    # Unique Graphic Style Collector
    for i in lineStyles:
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
            if i.Name[0:len(prefix)] == prefix and i.Id.IntegerValue > 0:
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

def AppendPrefixtoLines(doc):

    lineStyles = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
    names = {}
    styleName = []
    for i in lineStyles:
        if not i.Name[0:len(prefix)] == prefix and not i.Id.IntegerValue < 0:
            names[i.Name] = i
            styleName.append(i.Name)
    sel_styleName = forms.SelectFromList.show(styleName, button_name='Select Item', multiselect=True)
    sel_style = []
    for i in sel_styleName:
        sel_style.append(names[i])
    # Non-Standard Line Changer
    for i in sel_style:
            weight = i.GetLineWeight(GraphicsStyleType.Projection).ToString()
            pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
            if pattern is None:
                patternName = 'Solid'
            else:
                patternName = pattern.Name
            uniqueParam = weight + patternName
            categories = doc.Settings.Categories
            lineCat = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
            count = 0
            if not prefix + i.Name in styleName:
                newName = prefix + i.Name
            else:
                newName = prefix + i.Name + '-1'
            newLineStyleCat = categories.NewSubcategory(lineCat, newName)
            doc.Regenerate()
            newLineStyleCat.SetLineWeight(int(weight), GraphicsStyleType.Projection)
            newLineStyleCat.LineColor = i.LineColor
            try:
                newLineStyleCat.SetLinePatternId(pattern.Id, GraphicsStyleType.Projection)
            except:
                pass
            # Add new Line style to dictionary
            print('Appended Prefix to ' + i.Name + ' to ' '\'' +
                  newName + '\'')
            SetLineStyle(doc, i, newLineStyleCat)
            doc.Delete(i.Id)
# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'WARNING: will delete line styles ' \
          'Please do not use lightly,' \
          'Please make sure you can have ownership of line elements' \
          'Please rename lines you want to keep to ' \
          'the right format Example: PA - White'

uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Select Action Item
actionList = ['Append Prefix to selected Line Styles(protect)',
              'Delete Excess Line Styles',
              'Add PA - to Line Styles',]
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

# Transaction Start
t = Transaction(doc, 'Add PA prefix to Name')
t.Start()

if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False,
                yes=False,
                no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Append Prefix to selected Line Styles(protect)'in sel_action:
        try:
            AppendPrefixtoLines(doc)
        except:
            print("Fail 1")
    if 'Delete Excess Line Styles' in sel_action:
        list = CollectLineStylefromLine(doc)
        try:
            DeleteExcessLineStyles(doc, list)
        except:
            print("Fail 2")
    if 'Add PA - to Line Styles' in sel_action:
        list = CollectLineStylefromLine(doc)
        try:
            AddPrefixtoLines(doc)
        except:
            print("Fail 3")
    else:
        pass
t.Commit()