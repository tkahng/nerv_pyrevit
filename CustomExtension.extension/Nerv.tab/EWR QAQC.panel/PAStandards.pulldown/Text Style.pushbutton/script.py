from pyrevit.framework import List
from pyrevit import revit, DB, forms
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
     Color, BuiltInParameter, TextNote, TextNoteType
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application

# Define the prefix we want to track and add
prefix = 'PA - '

def SetTextStyle(doc, source, destination):
    elements = FilteredElementCollector(doc).OfClass(TextNote).ToElements()
    for i in elements:
        if i.LookupParameter('Type').AsValueString() == source:
            i.TextNoteType = destination
            # print(sourceLineStyle.Name + ' is being changed to ' + DestinationLineStyle.Name)

def CollectTextNoteFromDoc(doc):
    fills = FilteredElementCollector(doc).OfClass(TextNote).ToElements()
    # print(len(lines))
    collector = []
    for i in fills:
        name = i.LookupParameter('Type').AsValueString()
        if not name in collector:
            collector.append(name)
    return collector

def DeleteExcessFromDoc(doc, list):
    elements = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
    for i in elements:
        name = i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        if not name in list and name[0] != '<' and name[0:len(prefix)] != prefix and i.Id.IntegerValue > 0:
            try:
                print('Deleting Text Style ' + name)
                doc.Delete(i.Id)
            except:
                print('Failed to Delete ' + name)

def ConsolidateRegion(doc):
    styles = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
    _dict = {}
    paramList = []
    names = []
    # Unique Graphic Style Collector
    for i in styles:
        offset = i.LookupParameter('Leader/Border Offset').AsDouble()
        border = i.LookupParameter('Show Border').AsValueString()
        font = i.LookupParameter('Text Font').AsString()
        size = i.LookupParameter('Text Size').AsDouble()
        width = i.LookupParameter('Width Factor').AsDouble()
        lineWeight = i.LookupParameter('Line Weight').AsInteger()
        back = i.LookupParameter('Background').AsValueString()
        color = i.LookupParameter('Color').AsInteger()
        bold = i.LookupParameter('Bold').AsInteger()
        italic = i.LookupParameter('Italic').AsInteger()
        underline = i.LookupParameter('Underline').AsInteger()
        try:
            arrow = i.LookupParameter('Leader Arrowhead').AsElementId().IntegerValue
        except:
            arrow = 0
        name = i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        unique_param = str(offset) + str(border) + str(font) + str(size) + str(width) + str(lineWeight) + \
                       str(back) + str(color) + str(bold) + str(italic) + str(underline) + str(arrow)

        if not unique_param in paramList:
            paramList.append(unique_param)
            names.append(name)
            _dict[str(unique_param)] = name

    # Non-Standard Line Changer
    instances = FilteredElementCollector(doc).OfClass(TextNote).ToElements()
    for i in instances:
        name = i.LookupParameter('Type').AsValueString()
        type = i.TextNoteType
        try:
            typeName = type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        except:
            typeName = ''
        offset = type.LookupParameter('Leader/Border Offset').AsDouble()
        border = type.LookupParameter('Show Border').AsValueString()
        font = type.LookupParameter('Text Font').AsString()
        size = type.LookupParameter('Text Size').AsDouble()
        width = type.LookupParameter('Width Factor').AsDouble()
        lineWeight = type.LookupParameter('Line Weight').AsInteger()
        back = type.LookupParameter('Background').AsValueString()
        color = type.LookupParameter('Color').AsInteger()
        bold = type.LookupParameter('Bold').AsInteger()
        italic = type.LookupParameter('Italic').AsInteger()
        underline = type.LookupParameter('Underline').AsInteger()
        try:
            arrow = i.LookupParameter('Leader Arrowhead').AsElementId().IntegerValue
        except:
            arrow = 0
        try:
            uniqueParam = str(offset) + str(border) + str(font) + str(size) + str(width) + str(lineWeight) + \
                       str(back) + str(color) + str(bold) + str(italic) +str (underline) + str(arrow)
        except:
            uniqueParam = 0
        if uniqueParam in paramList and not name in names and typeName[0:len(prefix)] != prefix:
            i.get_Parameter(BuiltInParameter.ELEM_TYPE_PARAM).Set(_dict[str(uniqueParam)])
            print(name + 'changed to ' + _dict[str(uniqueParam)])

def Translator(element, text1, text2):
    if element == 0:
        return text1
    else:
        return text2

def FeettoInch(number):
    inch = (number) * 12 * 10
    inchInt = inch
    result = str(inchInt) + '\"' +'/10\"'
    return result

def AddPAtoText(doc):
    styles = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
    names = []
    dict ={}
    for i in styles:
        names.append(i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString())
    for i in styles:
        name = i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        if name[0:len(prefix)] != prefix and i.Id.IntegerValue > 0:
            try:
                proposedName = prefix + 'TEXT '+ FeettoInch(i.LookupParameter('Text Size').AsDouble()) + ' '+ \
                               i.LookupParameter('Background').AsValueString() + \
                               Translator(i.LookupParameter('Bold').AsInteger(),'', 'Bold') + ' ' + \
                               Translator(i.LookupParameter('Italic').AsInteger(),'', 'Italic') + ' '+ \
                               Translator(i.LookupParameter('Underline').AsInteger(), '', 'Underline') + ' ' + \
                               doc.GetElement(i.LookupParameter('Leader Arrowhead').AsElementId()).get_Parameter\
                                   (BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
                destination = i.Duplicate(proposedName)
                SetTextStyle(doc, name, destination)
                doc.Delete(i.Id)
                print('Renamed ' + name + ' to ' + proposedName)
                names.append(proposedName)
            except:
                proposedName = prefix + 'TEXT '+ name
                destination = i.Duplicate(proposedName)
                SetTextStyle(doc, name, destination)
                doc.Delete(i.Id)
                print('Renamed ' + name + ' to ' + proposedName)
                names.append(proposedName)

def SetAllTextNotetoArial(doc):
    styles = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
    for i in styles:
        font = i.LookupParameter('Text Font').AsString()
        if font != 'Arial Narrow':
            i.LookupParameter('Text Font').Set('Arial')
        else:
            i.LookupParameter('Text Font').Set('Arial')
            i.LookupParameter('Width Factor').Set(0.82)

def AppendPrefix(doc):

    styles = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
    names = {}
    styleName = []
    for i in styles:
        names[i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()] = i
        styleName.append(i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString())

    sel_styles = forms.SelectFromList.show(styleName, button_name='Select Item you want to add prefix to',
                                           multiselect=True)
    for i in sel_styles:
        name = names[i].get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        if name[0:len(prefix)] != prefix and names[i].Id.IntegerValue > 0:
            proposedName = prefix + name
            print(proposedName, names[i].Id.IntegerValue)
            destination = names[i].Duplicate(prefix + name)
            SetTextStyle(doc, name, destination)
            doc.Delete(names[i].Id)
            print('Appended Prefix to' + name + ' to ' + proposedName)

# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Modify Text Style, click to see more options ' \
          'Please do not use lightly'

uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Select Action Item
actionList = ['Append Prefix to selected(protect)',
              'Delete Excess Text Styles',
              'Set all text note to Arial',
              'Add PA - to Text Styles',
              ]
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

# Transaction Start
t = Transaction(doc, 'Add PA prefix to Name')
t.Start()

if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False,
                yes=False,
                no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Append Prefix to selected(protect)' in sel_action:
        AppendPrefix(doc)
    if 'Delete Excess Text Styles' in sel_action:
        list = CollectTextNoteFromDoc(doc)
        try:
            DeleteExcessFromDoc(doc, list)
        except:
            print("Fail 1")
    if 'Set all text note to Arial' in sel_action:
        try:
            SetAllTextNotetoArial(doc)
        except:
            print("Fail 2")
    if 'Add PA - to Text Styles' in sel_action:
        list = CollectTextNoteFromDoc(doc)

        ConsolidateRegion(doc)
        DeleteExcessFromDoc(doc, list)
        AddPAtoText(doc)
    else:
        pass
t.Commit()