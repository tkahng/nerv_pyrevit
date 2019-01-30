from pyrevit.framework import List
from pyrevit import revit, DB, forms
import clr, re
from fractions import Fraction
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
    CurveElement, Color
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

def AddPrefixtoAnnotation(doc):
        annotation = FilteredElementCollector(doc).OfClass(FamilySymbol)
        family = []
        familyName = []
        family_dict = {}
        for i in annotation:
            cate = i.Category.Name
            if cate == 'Generic Annotations' or 'Symbol' in cate or 'Tag' in cate or 'Annotation' in cate or 'Title' in cate:
                if str(i.Family.Name)[0:len(prefix)] != prefix and not i.Family in family:
                    familyName.append(i.Family.Name)
                    family.append(i.Family)
                    for i in range(len(family)):
                        family_dict[familyName[i]] = family[i]
        sel_family = forms.SelectFromList.show(familyName, button_name='Select Item you want to add prefix to',
                                               multiselect=True)
        if not sel_family is None:
            for f in sel_family:
                changed_name = []
                name = family_dict[f].Name
                if name[0:len(prefix)] != prefix:
                    if not prefix + name in changed_name:
                        family_dict[f].Name = prefix + name
                        changed_name.append(family_dict[f].Name)

# TODO Fix this function
def SetLineStyle(doc, sourceLineStyle, DestinationLineStyle):
    lines = FilteredElementCollector(doc).OfClass(CurveElement).ToElements()
    for i in lines:
        if i.LineStyle.Name == sourceLineStyle.Name:
            i.LineStyle = DestinationLineStyle.GetGraphicsStyle(GraphicsStyleType.Projection)
            # print(sourceLineStyle.Name + ' is being changed to ' + DestinationLineStyle.Name)

def CollectLineStylefromLine(doc):
    lines = FilteredElementCollector(doc).OfClass(CurveElement).ToElements()
    # print(len(lines))
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
        '''
        lineStyle.append(i.Name)
        lineStyle.append(i.LineColor.Red)
        lineStyle.append(i.LineColor.Green)
        lineStyle.append(i.LineColor.Blue)
        '''
        weight = i.GetLineWeight(GraphicsStyleType.Projection).ToString()
        pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
        if pattern is None:
            patternName = 'Solid'
        else:
            patternName = pattern.Name
        # unique parameter of line weight + line pattern as a parameter indicator
        uniqueParam = weight + patternName
        if not uniqueParam in paramList:
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
                newName = prefix + 'Pen # ' + str(weight) + ' ' +str(patternName)
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
                print(i.Name + ' changed to ' '\'' +
                      newName + '\'')
                SetLineStyle(doc, i, newLineStyleCat)
                doc.Delete(i.Id)


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


# Select Action Item
actionList = ['Add PA - to Annotation Symbol',
              'Delete Excess Line Styles',
              'Add PA - to Line Styles',
              'Add PA - to Filled Region']
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

# Transaction Start
t = Transaction(doc, 'Add PA prefix to Name')
t.Start()

if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Add PA - to Annotation Symbol' in sel_action:
        AddPrefixtoAnnotation(doc)
    if 'Delete Excess Line Styles' in sel_action:
        list = CollectLineStylefromLine(doc)
        DeleteExcessLineStyles(doc, list)
    if 'Add PA - to Line Styles' in sel_action:
        list = CollectLineStylefromLine(doc)
        AddPrefixtoLines(doc)
    if 'Add PA - to Filled Region' in sel_action:
        AddPrefixtoFilledRegion(doc)
    else:
        pass
t.Commit()