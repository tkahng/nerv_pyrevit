
import sys, clr
import ConfigParser
from os.path import expanduser
# Set system path
home = expanduser("~")
cfgfile = open(home + "\\STVTools.ini", 'r')
config = ConfigParser.ConfigParser()
config.read(home + "\\STVTools.ini")
# Master Path
syspath1 = config.get('SysDir','MasterPackage')
sys.path.append(syspath1)
# Built Path
syspath2 = config.get('SysDir','SecondaryPackage')
sys.path.append(syspath2)

from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle
from Autodesk.Revit.DB import Level, BuiltInParameter
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit import forms
import xlsxwriter

__doc__ = 'Export all Object Styles setting to an Excel file.'

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
def GetObjectStyleData(g):
    list = []
    list.append(g.GraphicsStyleCategory.CategoryType.ToString())
    list.append(g.Name)
    list.append(g.GraphicsStyleType.ToString())
    list.append(g.GraphicsStyleCategory.GetLineWeight(g.GraphicsStyleType).ToString())
    red = "N/A"
    green = "N/A"
    blue = "N/A"
    try:
        red = g.GraphicsStyleCategory.LineColor.Red.ToString()
        green = g.GraphicsStyleCategory.LineColor.Green.ToString()
        blue = g.GraphicsStyleCategory.LineColor.Blue.ToString()
    except:
        pass

    list.append(red)
    list.append(green)
    list.append(blue)
    list.append(g.GraphicsStyleCategory.GetLinePatternId(g.GraphicsStyleType).ToString())
    try:
        list.append(g.GraphicsStyleCategory.Material.Name)
    except:
        pass
    return list
def GetCategoryData(parent, g, type):
    list = []
    list.append(parent)
    list.append(g.Name)
    list.append(type.ToString())
    try:
        list.append(g.GetLineWeight(type).ToString())
    except:
        list.append("")
    red = "N/A"
    green = "N/A"
    blue = "N/A"
    try:
        red = g.LineColor.Red.ToString()
        green = g.LineColor.Green.ToString()
        blue = g.LineColor.Blue.ToString()
    except:
        pass

    list.append(red)
    list.append(green)
    list.append(blue)
    list.append(g.GetLinePatternId(type).ToString())
    try:
        list.append(g.Material.Name)
    except:
        pass
    return list
destinationFolder = forms.pick_folder()
gStyle = FilteredElementCollector(doc).OfClass(GraphicsStyle).ToElements()
collectionInvalid = [['Category Type', 'Category', 'Type', 'Line Weight', 'R', 'G', 'B', 'Pattern', 'Material']]
collectionModel = [['Category Type', 'Category', 'Type', 'Line Weight', 'R', 'G', 'B', 'Pattern', 'Material']]
collectionAnno = [['Category Type', 'Category', 'Type', 'Line Weight', 'R', 'G', 'B', 'Pattern', 'Material']]
collectionInternal = [['Category Type', 'Category', 'Type', 'Line Weight', 'R', 'G', 'B', 'Pattern', 'Material']]
collectionAnalytical = [['Category Type', 'Category', 'Type', 'Line Weight', 'R', 'G', 'B', 'Pattern', 'Material']]
for g in gStyle:
    workSet = g.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
    if workSet == "Object Styles" and not g.GraphicsStyleCategory.Parent:
        type = g.GraphicsStyleCategory.CategoryType.ToString()
        list = GetObjectStyleData(g)
        if type == "Invalid":
            collectionInvalid.append(list)
        elif type == "Model":
            collectionModel.append(list)
        elif type == "Annotation":
            collectionAnno.append(list)
        elif type == "Internal":
            collectionInternal.append(list)
        elif type == "AnalyticalModel":
            collectionAnalytical.append(list)

        if not g.GraphicsStyleCategory.SubCategories.IsEmpty:
            for i in g.GraphicsStyleCategory.SubCategories:
                subList = [i.Name]
                if type == "Invalid":
                    collectionInvalid.append(GetCategoryData(g.Name, i, g.GraphicsStyleType))
                elif type == "Model":
                    collectionModel.append(GetCategoryData(g.Name, i, g.GraphicsStyleType))
                elif type == "Annotation":
                    collectionAnno.append(GetCategoryData(g.Name, i, g.GraphicsStyleType))
                elif type == "Internal":
                    collectionInternal.append(GetCategoryData(g.Name, i, g.GraphicsStyleType))
                elif type == "AnalyticalModel":
                    collectionAnalytical.append(GetCategoryData(g.Name, i, g.GraphicsStyleType))

fileName = destinationFolder + '\\' + doc.Title + '.xlsx'
excelFile = ExcelOpener(fileName)
ExcelWriter(excelFile, 'Invalid', 0, 0, collectionInvalid)
ExcelWriter(excelFile, 'Model', 0, 0, collectionModel)
ExcelWriter(excelFile, 'Annotation', 0, 0, collectionAnno)
ExcelWriter(excelFile, 'Internal', 0, 0, collectionInternal)
ExcelWriter(excelFile, 'AnalyticalModel', 0, 0, collectionAnalytical)


excelFile.close()
print(fileName + " Completed")
'''
    params = Selection.get_all_parameters_as_dic(g).keys()
    values = Selection.get_all_parameters_as_dic(g).values()
    count = 0
    for i in params:
        list.append(i)# + ' : ' + values[count])
        count += 1
    collection.append(list)
for i in collection:
    print('----------------------')
    for a in i:
        print(a)
        '''