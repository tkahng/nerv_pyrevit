
import clr
import xlsxwriter

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Document, BuiltInCategory, GraphicsStyleType, FilteredElementCollector, Level, \
    ElementWorksetFilter, WorksetKind, FilteredWorksetCollector, ImportInstance
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
        linkName.append(i.Id)
        try:
            linkPin.append(str(i.Pinned))
        except:
            linkPin.append("Error")
    count = 0
    for i in linkName:
        docLink.append(linkName[count])
        docLink.append(linkName[count])
        count += 1