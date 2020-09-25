from pyrevit.framework import List
from pyrevit import revit, DB, forms
import clr, time, re
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
    CurveElement, Color, BuiltInParameter, LinePatternElement
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


def DeleteExcessLineStyles(doc, list, start_time, limit):
    lineStyle = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
    standard = {}
    for i in lineStyle:
        # individual transactions
        t = Transaction(doc, 'Delete Excess Line Styles')
        t.Start()
        if not i.Name in list and i.Name[0] != '<' and i.Id.IntegerValue > 0 and time.time()-start_time < limit:
            try:
                if i.Name[0:5] == prefix:
                    standard[i.Name] = i
                else:
                    print('Deleting Line Style ' + i.Name)
                    doc.Delete(i.Id)

            except:
                print('Failed to Delete ' + i.Name)
        t.Commit()

    sel_delete = forms.SelectFromList.show(standard.keys(), button_name='Select Item', multiselect=True)
    for s in sel_delete:
        if time.time()-start_time < limit:
            t = Transaction(doc, 'Delete Excess Line Styles')
            t.Start()
            print('Deleting Line Style ' + standard[s].Name)
            doc.Delete(standard[s].Id)
            t.Commit()

class NervLinePattern:
    kind = 'canine'  # class variable shared by all instances

    def __init__(self, inTypes, inLength):
        self.types = inTypes  # instance variable unique to each instance
        self.length = inLength  # instance variable unique to each instance

def difference (list1, list2):
   list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
   return list_dif

def DeleteExcessLinePatterns(doc, start_time, limit):
    lineStyle = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
    usedPattern = []
    for i in lineStyle:
        pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
        if not pattern in usedPattern:
            usedPattern.append(pattern)
    patterns = FilteredElementCollector(doc).OfClass(LinePatternElement).ToElements()
    for p in patterns:
        if not p in usedPattern:
            try:
                t = Transaction(doc, 'Delete Line Patterns')
                t.Start()
                if "IMPORT" in p.GetLinePattern().Name:
                    print("Deleting " + p.GetLinePattern().Name)
                    doc.Delete(p.Id)
                t.Commit()
            except:
                pass

def ConsolidateExcessLinePatterns(doc, start_time, limit):

    all = []
    lineStyle = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
    usedPattern = []
    for i in lineStyle:
        uniquedata = []
        pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
        if not pattern in usedPattern:
            usedPattern.append(pattern)
        try:
            segments = pattern.GetLinePattern().GetSegments()
        except:
            segments = []
        types = ''
        length = []
        for s in segments:
            length.append(s.Length)
            types += str(s.Type)
        try:
            try:
                uniquedata.append(i)
                uniquedata.append(pattern.GetLinePattern().Name)
                uniquedata.append(types)
                uniquedata.append(length)
                uniquedata.append(pattern)
            except:
                uniquedata.append(i)
                uniquedata.append(pattern.GetLinePattern().Name)
                uniquedata.append('Solid')
                uniquedata.append([0])
                uniquedata.append('Solid')
        except:
            uniquedata.append(i)
            uniquedata.append('Solid')
            uniquedata.append('Solid')
            uniquedata.append([0])
            uniquedata.append('Solid')
        all.append(uniquedata)

    patterns = FilteredElementCollector(doc).OfClass(LinePatternElement).ToElements()
    allPattern = []

    for pattern in patterns:
        uniquedata = []
        try:
            segments = pattern.GetLinePattern().GetSegments()
        except:
            segments = []
        types = ''
        length = []
        for s in segments:
            length.append(s.Length)
            types += str(s.Type)
        try:
            try:
                uniquedata.append(pattern.GetLinePattern().Name)
                uniquedata.append(types)
                uniquedata.append(length)
                uniquedata.append(pattern)
            except:

                uniquedata.append(pattern.GetLinePattern().Name)
                uniquedata.append('Solid')
                uniquedata.append([0])
                uniquedata.append('Solid')
        except:
            uniquedata.append('Solid')
            uniquedata.append('Solid')
            uniquedata.append([0])
            uniquedata.append('Solid')

        allPattern.append(uniquedata)

    changeList = {}
    for pattern in patterns:
        try:
            segments = pattern.GetLinePattern().GetSegments()
        except:
            segments = []
        types = ''
        length = []
        for s in segments:
            length.append(s.Length)
            types += str(s.Type)
        for i in allPattern:
            if i[0] != pattern.GetLinePattern().Name and i[1] == types and i[2] == length and i[3] != pattern and \
                    not i[0] in changeList.keys() and not "IMPORT" in i[3].GetLinePattern().Name and pattern != "Solid":
                changeList[pattern.GetLinePattern().Name] = i[3]
    nameDic = []
    for i in changeList.keys():
        # print(i)
        print(i + " change to " + changeList[i].GetLinePattern().Name)
    for c in changeList.keys():
        # print(i)
        nameDic.append(c)

    for a in all:
        print("------------")
        name = ""
        try:
            name = a[4].GetLinePattern().Name
        except:
            name = ""

        if name in nameDic and name != "":
            print(a[4])
            t = Transaction(doc, 'Change Line Style Pattern')
            t.Start()
            a[0].SetLinePatternId(changeList[name].Id, GraphicsStyleType.Projection)
            # a[0].Name = re.split("IMPORT-", a[0].Name)[0] + " " + changeList[name].GetLinePattern().Name
            print("Changed " + a[0].Name + ' to ' + changeList[name].GetLinePattern().Name)
            t.Commit()


    # for a in all:
        # if a

def AddPrefixtoLines(doc, start_time, limit):
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
        t = Transaction(doc, 'Add PA prefix to Name')
        t.Start()
        if not i.Name[0:len(prefix)] == prefix and not i.Id.IntegerValue < 0 and time.time()-start_time < limit:
            weight = i.GetLineWeight(GraphicsStyleType.Projection).ToString()
            pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
            if pattern is None:
                patternName = 'Solid'
            else:
                patternName = pattern.Name
            uniqueParam = weight + patternName
            # Try changing it to an existing line style in dictionary
            # if line_dict[uniqueParam]:
            try:
                SetLineStyle(doc, i, line_dict[uniqueParam])
                print('Changed ' + i.Name + ' to ' + line_dict[uniqueParam].Name)
                doc.Delete(i.Id)
            # Create a new, properly named Line Style
            except:
            # else:
                categories = doc.Settings.Categories
                lineCat = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
                newName = prefix + 'Pen # ' + str(weight) + ' ' + str(patternName)
                #try:
                newLineStyleCat = categories.NewSubcategory(lineCat, newName)
                doc.Regenerate()
                newLineStyleCat.SetLineWeight(int(weight), GraphicsStyleType.Projection)
                newLineStyleCat.LineColor = Color(0x00, 0x00, 0x00)
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
                #except:
                    #print('Contains wrong characters ' + '\'' + i.Name + '\'')
        t.Commit()
def AppendPrefixtoLines(doc, start_time, limit):

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
        t = Transaction(doc, 'Add PA prefix to Name')
        t.Start()
        if time.time()-start_time < limit:
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
            try:
                SetLineStyle(doc, i, newLineStyleCat)
                doc.Delete(i.Id)
            except:
                print('Fail to set line, maybe it contains prohibited characters.')
        t.Commit()
def MergeLines(doc, start_time, limit):
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
            if i.Id.IntegerValue > 0:
                # Create standard line style dictionary
                line_dict[uniqueParam] = i
                paramList.append(uniqueParam)
    print(line_dict.keys())
    print(line_dict.values())
    # Non-Standard Line Changer
    for i in lineStyles:
        t = Transaction(doc, 'Merge Line Styles')
        t.Start()
        if not i.Id.IntegerValue < 0 and time.time()-start_time < limit:
            weight = i.GetLineWeight(GraphicsStyleType.Projection).ToString()
            pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
            if pattern is None:
                patternName = 'Solid'
            else:
                patternName = pattern.Name
                print(patternName)
            uniqueParam = weight + patternName
            # Try changing it to an existing line style in dictionary
            # if line_dict[uniqueParam]:
            try:
                SetLineStyle(doc, i, line_dict[uniqueParam])
                # print('Changed ' + i.Name + ' to ' + line_dict[uniqueParam].Name)
                # doc.Delete(i.Id)
            # Create a new, properly named Line Style
            except:
                print('fail')
        t.Commit()
# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Modify line types, click to see more options.' \
          'WARNING: will delete line styles ' \
          'Please do not use lightly,' \
          'Please make sure you can have ownership of line elements' \
          'Please rename lines you want to keep to ' \
          'the right format Example: PA - White'

uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Select Action Item
actionList = ['Append Prefix to selected Line Styles(protect)',
              'Delete Excess Line Styles',
              'Delete Excess Line Patterns',
            'Consolidate Excess Line Patterns',
              'Merge Line Styles',
              'Add PA - to Line Styles',
              ]
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

# Transaction Start
# t = Transaction(doc, 'Add PA prefix to Name')
# t.Start()
start_time = time.time()
limit = 300
print(start_time)
if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False,
                yes=False,
                no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Append Prefix to selected Line Styles(protect)'in sel_action:
        try:
            AppendPrefixtoLines(doc, start_time, limit)
        except:
            print("Fail 1")
    if 'Delete Excess Line Styles' in sel_action:
        list = CollectLineStylefromLine(doc)
        try:
            DeleteExcessLineStyles(doc, list, start_time, limit)
        except:
            print("Fail 2")
    if 'Delete Excess Line Patterns' in sel_action:
        DeleteExcessLinePatterns(doc, start_time, limit)
    if 'Consolidate Excess Line Patterns' in sel_action:
        ConsolidateExcessLinePatterns(doc, start_time, limit)
    if 'Merge Line Styles' in sel_action:
        MergeLines(doc, start_time, limit)
    if 'Add PA - to Line Styles' in sel_action:
        list = CollectLineStylefromLine(doc)
        #try:
        AddPrefixtoLines(doc, start_time, limit)
        #except:
            #print("Fail 3")
    else:
        pass
print(time.time())
if time.time() - start_time > limit:
    print("Script Time Out!! The process is stopped due to the mass of the process might hang you revit for more than 4 hrs"
          "Please run the Tool again until you do not see this message to complete clan up")
print('Done')
# t.Commit()