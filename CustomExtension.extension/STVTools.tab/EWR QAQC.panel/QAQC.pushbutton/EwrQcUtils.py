import re
import clr
import xlsxwriter

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Document, BuiltInCategory, GraphicsStyleType, FilteredElementCollector, Level, \
    ElementWorksetFilter, WorksetKind, FilteredWorksetCollector, ImportInstance, FilledRegionType,\
    BuiltInParameter, FamilySymbol, UnitType, DimensionType, Viewport, CategoryType, RevitLinkInstance, RevitLinkType
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')

def WorksetElements(doc, workset):
	elementCollector = FilteredElementCollector(doc)
	elementWorksetFilter = ElementWorksetFilter(workset.Id, False)
	worksetElemsfounds = elementCollector.WherePasses(elementWorksetFilter).ToElements()
	return worksetElemsfounds

def ExcelOpener(fileName):
    workbook = xlsxwriter.Workbook(fileName)
    return workbook

def ExcelWriter(workbook, SheetName, startRow, startCol, list):
    worksheet = workbook.add_worksheet(SheetName)
    row = startRow
    for rowItems in list:
        col = startCol
        for item in rowItems:
            worksheet.write(row, col, item)
            col += 1
        row += 1

def LineCheck(doc):
    lines = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
    out = []
    for i in lines:
        lineStyle = []
        lineStyle.append(i.Name)
        lineStyle.append(i.LineColor.Red)
        lineStyle.append(i.LineColor.Green)
        lineStyle.append(i.LineColor.Blue)
        lineStyle.append(i.GetLineWeight(GraphicsStyleType.Projection))
        pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
        if pattern is None:
            lineStyle.append('Solid')
        else:
            lineStyle.append(pattern.Name)
        out.append(lineStyle)
    return out

def LevelCheck(doc):
    levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
    out = []
    for i in levels:
        out.append([i.Name])
    return out

def SheetElementCheck(doc):
    model = []
    worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.ViewWorkset).ToWorksets()
    sheets = []
    names = []
    sheetWorkset = []
    for workset in worksets:
        if workset.Name[6:11] == 'Sheet':
            sheetWorkset.append(workset)
    for ws in sheetWorkset:
        sheet = []
        name = []
        sheet.append(ws.Name)
        elems = WorksetElements(doc, ws)
        i = 1
        while i < len(elems):
            sheet.append(ws.Name)
            i += 1
        for elem in elems:
            try:
                name.append(elem.GetType().ToString() + '     ' + elem.Name)
            except:
                name.append(elem.GetType().ToString() + '     ' + str(elem))
        sheets.append(sheet)
        names.append(name)
    flat_sheets = [item for sublist in sheets for item in sublist]
    flat_names = [item for sublist in names for item in sublist]
    count = 0
    for i in flat_sheets:
        group = []
        group.append(flat_sheets[count])
        group.append(flat_names[count])
        model.append(group)
        count += 1
    return model

def CadImportsCheck(doc):
    docLink = []
    collector = FilteredElementCollector(doc)
    linkInstances = collector.OfClass(ImportInstance)
    linkName, linkPin = [], []
    for i in linkInstances:
        linkName.append(str(i.Id.IntegerValue))
        try:
            linkPin.append(str(i.Pinned))
        except:
            linkPin.append("Error")
    count = 0
    for i in linkName:
        line = []
        line.append(linkName[count])
        line.append(linkPin[count])
        docLink.append(line)
        count += 1
    return docLink


def FilledRegionCheck(doc):
    instances = FilteredElementCollector(doc).OfClass(FilledRegionType).ToElements()
    name = []
    for i in instances:
        id = i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        name.append([id])
    return name

def AnnotationSymbolCheck(doc):
    collector = FilteredElementCollector(doc)
    instances = collector.OfClass(FamilySymbol)
    name = []
    for i in instances:
        cate = i.Category.Name
        if cate == 'Generic Annotations' or 'Symbol' in cate or 'Tag' in cate or 'Annotation' in cate:
            name.append([i.Family.Name])
    return(name)

def SettingsCheck(doc):
    unit = ['Tolerance']
    unit.append(doc.GetUnits().GetFormatOptions(UnitType.UT_Length).Accuracy * 12)
    phases = ['Phases']
    for i in doc.Phases:
        phases.append(i.Name)
    out = []
    out.append(unit)
    out.append(phases)
    return out

def DimensionsCheck(doc):
    modelLst = []
    dimensions = FilteredElementCollector(doc).OfClass(DimensionType).ToElements()
    units = doc.GetUnits().GetFormatOptions(UnitType.UT_Length).Accuracy
    for i in dimensions:
        parameters = []
        try:
            method = str(i.GetUnitsFormatOptions().Accuracy * 12)
        except:
            method = str(units * 12)
        try:
            name = i.LookupParameter('Type Name').AsString()
            textFont = i.LookupParameter('Text Font').AsString()
            parameters.append(name)
            parameters.append(textFont)
            parameters.append(method)
            modelLst.append(parameters)
        except:
            pass
        '''
        param = i.Parameters
        for p in param:
            print(p.AsString())
            print('Name: ' + str(p.Definition.Name))
        '''
    return modelLst

def SheetsCheck(doc):
    modelLst = []
    viewports = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
    for i in viewports:
        parameters = []
        name = i.LookupParameter('Sheet Name').AsString()
        viewClassification = i.LookupParameter('PA - View Classification').AsString()
        number = i.LookupParameter('Sheet Number').AsString()
        disGroup = i.LookupParameter('Discipline Group').AsString()
        subDisGroup = i.LookupParameter('Discipline Sub-Group').AsString()
        appearSheet = i.LookupParameter('Appears In Sheet List').AsString()
        parameters.append(number)
        parameters.append(name)
        parameters.append(viewClassification)
        parameters.append(appearSheet)
        parameters.append(disGroup)
        parameters.append(subDisGroup)

        modelLst.append(parameters)
    return modelLst

def ViewsCheck(doc):
    modelLst = []
    viewports = FilteredElementCollector(doc).OfClass(Viewport).ToElements()
    for i in viewports:
        parameters = []
        name = i.LookupParameter('View Name').AsString()
        viewClassification = i.LookupParameter('PA - View Classification').AsString()
        parameters.append(name)
        parameters.append(viewClassification)
        modelLst.append(parameters)
    return modelLst

def WorksetCheck(doc):
    # create workset collector
    userWorksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
    # extract workset's name and ids
    modelLst = []
    for i in userWorksets:
        line = []
        line.append(i.Name)
        line.append(i.IsVisibleByDefault)
        modelLst.append(line)
    return modelLst

def FamilyNameCheck(doc):
    modelLst = []
    family = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
    exempt = ['Profiles', 'Section Marks', 'Curtain Panels', 'Section Marks', 'Generic Annotations', 'Callout Heads',
              'Level Heads', 'View Titles']
    for i in family:
        line = []
        if not i.Family.FamilyCategory.Name in exempt and not 'Tag' in i.Family.FamilyCategory.Name:
            line.append(i.Family.FamilyCategory.Name)
            line.append(i.Family.Name)
            modelLst.append(line)
    return modelLst

def LinkCheck(doc):
    LinkObj = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
    LinkTyp = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
    modelLst = []
    count = 0
    for a in LinkObj:
        line = []
        name = a.Name
        linkSoup = re.split(':', name)
        linkName = linkSoup[0]
        linkLocation = linkSoup[2]
        workset = a.LookupParameter('Workset').AsValueString()
        attachmentType = LinkTyp[count].AttachmentType
        line.append(linkName)
        line.append(linkLocation)
        line.append(workset)
        line.append(str(a.Pinned))
        line.append(str(attachmentType))
        modelLst.append(line)
        count +=1
    return modelLst

def TitleBlockCheck(doc):
    modelLst = []
    titleBlock = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).ToElements()
    for i in titleBlock:
        line = []
        try:
            sheetNumber = i.LookupParameter('Sheet Number').AsString()
            line.append(sheetNumber)
        except:
            pass
        try:
            familyName = i.LookupParameter('Family').AsValueString()
            line.append(str(familyName))
        except:
            pass
        if line != []:
            modelLst.append(line)
    return modelLst