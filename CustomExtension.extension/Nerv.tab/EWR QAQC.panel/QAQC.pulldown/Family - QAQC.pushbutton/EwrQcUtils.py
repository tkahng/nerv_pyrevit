import re
import clr
from pyrevit.framework import List
from pyrevit import revit, DB, forms
import xlsxwriter
import math
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import Document, BuiltInCategory, GraphicsStyleType, FilteredElementCollector, Level, \
    ElementWorksetFilter, WorksetKind, FilteredWorksetCollector, ImportInstance, FilledRegionType,\
    BuiltInParameter, FamilySymbol, UnitType, DimensionType, Viewport, CategoryType, RevitLinkInstance, RevitLinkType, \
    ViewSheet, TextElement, TextNoteType, XYZ, BasePoint, Transform, AnnotationSymbol
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
        if i.Id.IntegerValue > 0:
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
    sheetWorkset = []
    for workset in worksets:
        if workset.Name[6:11] == 'Sheet':
            sheetWorkset.append(workset)
    for ws in sheetWorkset:
        sheet = ws.Name
         # sheet.append(ws.Name)
        elems = WorksetElements(doc, ws)
        for elem in elems:
            name = []
            try:
                name.append(sheet)
                name.append(elem.GetType().ToString() + '     ' + elem.Name)
            except:
                name.append(sheet)
                name.append(elem.GetType().ToString() + '     ' + str(elem))
            model.append(name)
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
        try:
            try:
                viewClassification = i.LookupParameter('PA - View Classification').AsString()
            except:
                viewClassification = i.LookupParameter('View Classification').AsString()
        except:
            viewClassification = 'View Classification Error'
        number = i.LookupParameter('Sheet Number').AsString()
        try:
            disGroup = i.LookupParameter('Discipline Group').AsString()
        except:
            disGroup = 'No Value'
        try:
            subDisGroup = i.LookupParameter('Discipline Sub-Group').AsString()
        except:
            subDisGroup = 'No Value'
        appearSheet = i.LookupParameter('Appears In Sheet List').AsValueString()
        parameters.append(number)
        parameters.append(name)
        if not viewClassification is None:
            parameters.append(viewClassification)
        else:
            parameters.append('No Value')
        parameters.append(str(appearSheet))
        if not disGroup is None:
            parameters.append(disGroup)
        else:
            parameters.append('No Value')
        if not subDisGroup is None:
            parameters.append(subDisGroup)
        else:
            parameters.append('No Value')

        modelLst.append(parameters)
    return modelLst

def ViewsCheck(doc):
    modelLst = []
    viewports = FilteredElementCollector(doc).OfClass(Viewport).ToElements()
    for i in viewports:
        parameters = []
        name = i.LookupParameter('View Name').AsString()
        try:
            viewClassification = i.LookupParameter('PA - View Classification').AsString()
        except:
            viewClassification = i.LookupParameter('View Classification').AsString()
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
              'Level Heads', 'View Titles','Spot Elevation Symbols', 'Grid Heads', 'Detail Items', 'Title Blocks',
              'Elevation Marks', 'View Reference', 'Mass']
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
        try:
            linkLocation = linkSoup[2]
        except:
            linkLocation = 'Location Error'
        workset = a.LookupParameter('Workset').AsValueString()
        try:
            attachmentType = LinkTyp[count].AttachmentType
        except:
            attachmentType = 'Multiple instance of link found Link Obj: ' + str(len(LinkObj)) + \
                             'Link Type: '+ str(len(LinkTyp))
        line.append(linkName)
        line.append(linkLocation)
        line.append(workset)
        if a.Pinned == True:
            line.append('Pinned')
        else:
            line.append('Not Pinned')
        line.append(str(attachmentType))
        modelLst.append(line)
        count += 1
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

def TextCheck(doc):
    modelLst = []
    textNoteType = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
    textElement = FilteredElementCollector(doc).OfClass(TextElement).ToElements()
    parameters = ["Type Name", "Text Font", "Text Size", "Tab Size", "Bold", "Italic",
                  "Underline","Width Factor", "Show Border", "Background", "Color"]
    textInstance = []
    unique = []

    for t in textElement:
        type = t.LookupParameter('Type').AsValueString()
        textInstance.append(type)
        if not type in unique:
            unique.append(type)
    dic = {}
    for u in unique:
        count = textInstance.count(u)
        dic[u] = str(count)

    for i in textNoteType:
        line = []
        for p in parameters:
            value = i.LookupParameter(p)
            if value.AsValueString():
                line.append(value.AsValueString())
            else:
                line.append(value.AsString())
        try:
            line.append(dic[i.LookupParameter('Type Name').AsString()])
        except:
            line.append('0')
        modelLst.append(line)
    return modelLst

def PositionCheck(doc):
    modelLst = []
    line = ['Shared Point']
# Survey Point
    survey = []
    base = []
    outProjBasePt = []
    outProjSurvPt = []
    outProjLoc = []
    ft2mm = 304.8
    coll = FilteredElementCollector(doc)
    basePt = coll.OfClass(BasePoint).ToElements()
    for e in basePt:
        a = e.Category.Name
        if a == "Project Base Point":
            outProjBasePt.append('Project Base Point"')
            pbpEW = e.LookupParameter("E/W")
            pbpNS = e.LookupParameter("N/S")
            pbpElev = e.LookupParameter("Elev")
            pbpAngle = e.LookupParameter("Angle to True North")
            outProjBasePt.append(str(round(pbpEW.AsDouble(), 6)))
            outProjBasePt.append(str(round(pbpNS.AsDouble(), 6)))
            outProjBasePt.append(str(round(pbpElev.AsDouble(), 6)))
            outProjBasePt.append(str(round(pbpAngle.AsDouble() * 180 / math.pi, 6)))
            outProjBasePt.append('N/A')
            outProjBasePt.append('N/A')
            outProjBasePt.append('N/A')
        elif a == "Survey Point":
            outProjSurvPt.append('Project Survey Point')
            pspEW = e.LookupParameter("E/W")
            pspNS = e.LookupParameter("N/S")
            pspElev = e.LookupParameter("Elev")
            outProjSurvPt.append(str(round(pspEW.AsDouble(), 6)))
            outProjSurvPt.append(str(round(pspNS.AsDouble(), 6)))
            outProjSurvPt.append(str(round(pspElev.AsDouble(), 6)))
            outProjSurvPt.append('N/A')
            outProjSurvPt.append('N/A')
            outProjSurvPt.append('N/A')
            outProjSurvPt.append('N/A')
    projLoc = doc.ActiveProjectLocation
    origin = XYZ(0.0, 0.0, 0.0)

    projPos = projLoc.get_ProjectPosition(origin)
    if projPos == None:
        outProjLoc.append("No Project Position at origin point")
    else:
        outProjLoc.append(round(projPos.EastWest * ft2mm, 6))
        outProjLoc.append(round(projPos.NorthSouth * ft2mm, 6))
    modelLst.append(outProjBasePt)
    modelLst.append(outProjSurvPt)
# Shared Point
    shared = ()
    SharedPoint = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Site).ToElements()
    for i in SharedPoint:
        try:
            if 'Shared' in i.Name:
                shared = i
        except:
            pass
    try:
        location = LocationShift(doc,shared.Location.Point)
        line.append(str(location.X))
        line.append(str(location.Y))
        line.append(str(location.Z))
        line.append('N/A')
        if shared.Pinned == True:
            line.append('Pinned')
        else:
            line.append('Not Pinned')
        discipline = shared.LookupParameter('Discipline').AsString()
        line.append(discipline)
        workset = shared.LookupParameter('Workset').AsValueString()
        line.append(workset)
    except:
        line.append('Error')
        line.append('Error')
        line.append('Error')
        line.append('N/A')
        line.append('Error')
        line.append('Error')
        line.append('Error')
    modelLst.append(line)
    return modelLst

def LocationShift(doc, point):
    cPoint = point
    basePt = doc.ActiveProjectLocation.GetProjectPosition(XYZ(0, 0, 0))
    ew = basePt.EastWest
    ns = basePt.NorthSouth
    ele = basePt.Elevation
    angle = basePt.Angle
    basexyz = [ew, ns, ele, angle]

    rotationTransform = Transform.CreateRotation(XYZ.BasisZ, angle)
    translationVector = XYZ(ew, ns, ele)
    translationTransform = Transform.CreateTranslation(translationVector)
    finalTransform = translationTransform.Multiply(rotationTransform)

    aPoint = Transform.CreateRotation(XYZ.BasisZ, angle).OfPoint(XYZ(cPoint.X, cPoint.Y, cPoint.Z))
    bPoint = XYZ(aPoint.X + ew, aPoint.Y + ns, aPoint.Z + ele)
    return(bPoint)

def CateinWorksetCheck(doc):
    modelLst = []
    allModel = FilteredElementCollector(doc) \
        .WhereElementIsNotElementType() \
        .ToElements()
    allLst = []
    for instance in allModel:
        cate = instance.Category
        if str(cate) != 'None':
            a = str(cate.Name)
            if instance.GetType() != AnnotationSymbol and str(cate.CategoryType) == 'Model' and \
                    str(cate.Name) != 'Detail Items' and cate.AllowsBoundParameters == True and a != 'Sheets' \
                    and a != 'Materials' and a != 'RVT Links' and a != 'Areas' and a != 'Project Information':

                workset = instance.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
                combine = str(cate.Name) + ' : ' + str(workset)
                if not combine in allLst:
                    allLst.append(combine)
    for i in allLst:
        a = re.split(' : ', i)
        modelLst.append(a)
    return modelLst