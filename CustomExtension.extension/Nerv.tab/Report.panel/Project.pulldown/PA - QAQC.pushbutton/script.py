import sys
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
from pyrevit.framework import List
from pyrevit import revit, DB, forms
import re, clr, os, threading
import EwrQcUtils
import xlsxwriter
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
	OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,\
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions
from System.Collections.Generic import List
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application
clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')
# Collect Save location and Rvt Files
collectorFiles = forms.pick_file(file_ext='rvt', multi_file=True, unc_paths=False)
destinationFolder = forms.pick_folder()

def RVTFileCollector(dir):
    files = []
    for file in os.listdir(dir):
        if file.endswith(".rvt"):
            #print(str(file))
            files.append(str(file))
    return files

def OpenFiles(oFile, app, audit):

    openOpt = OpenOptions()
    if audit == True:
        openOpt.Audit = True
    else:
        openOpt.Audit = False
    openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    wsopt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
    # wsopt.Open(worksetList)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(oFile)
    currentdoc = app.OpenDocumentFile(modelPath, openOpt)
    try:
        DialogBoxShowingEventArgs.OverrideResult(1)
    except:
        pass
    return currentdoc


# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Report the Model Element Quality Check outcome in an Excel file according to PA standard.'

uiapp = UIApplication(doc.Application)
application = uiapp.Application
def DimensionProcessing(openedDoc):
    collectorDim = EwrQcUtils.DimensionsCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'DIMENSIONS', 1, 0, collectorDim)
def SettingsProcessing(openedDoc):
    collectorSettings = EwrQcUtils.SettingsCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'SETTINGS', 1, 0, collectorSettings)
def ViewsProcessing(openedDoc):
    collectorView = EwrQcUtils.ViewsCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'VIEWS', 1, 0, collectorView)
def FamiliesProcessing(openedDoc):
    collectorFamily = EwrQcUtils.FamilyNameCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'FAMILY NAME', 1, 0, collectorFamily)
def LinksProcessing(openedDoc):
    collectorLink = EwrQcUtils.LinkCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'LINKS', 1, 0, collectorLink)
def TitleBlocksProcessing(openedDoc):
    collectorTitleBlock = EwrQcUtils.TitleBlockCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'TITLE BLOCK', 1, 0, collectorTitleBlock)
def SheetsProcessing(openedDoc):
    collectorSheet = EwrQcUtils.SheetsCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'SHEETS', 1, 0, collectorSheet)
def TextsProcessing(openedDoc):
    collectorText = EwrQcUtils.TextCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'TEXT STYLE', 1, 0, collectorText)
def PositionProcessing(openedDoc):
    collectorPosition = EwrQcUtils.PositionCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'PROJECT INFO', 1, 0, collectorPosition)
def CateinWorksetsProcessing(openedDoc):
    collectorCateinWorkset = EwrQcUtils.CateinWorksetCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'CATEGORIES IN WORKSETS', 1, 0, collectorCateinWorkset)
def LevelsProcessing(openedDoc):
    collectorLevels = EwrQcUtils.LevelCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'LEVEL', 1, 0, collectorLevels)
def SheetElementsProcessing(openedDoc):
    collectorSheetElements = EwrQcUtils.SheetElementCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'SHEET ELEMENT', 1, 0, collectorSheetElements)
def LinesProcessing(openedDoc):
    collectorLines = EwrQcUtils.LineCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'LINE', 1, 0, collectorLines)
def FilledRegionsProcessing(openedDoc):
    collectorFilledRegion = EwrQcUtils.FilledRegionCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'FILLED REGIONS', 1, 0, collectorFilledRegion)
def AnnotationsProcessing(openedDoc):
    collectorAnnotationSymbol = EwrQcUtils.AnnotationSymbolCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'ANNOTATION SYMBOLS', 1, 0, collectorAnnotationSymbol)
def CadImportsProcessing(openedDoc):
    collectorCADImports = EwrQcUtils.CadImportsCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'CAD LINKS AND IMPORTS', 1, 0, collectorCADImports)
def WorksetsProcessing(openedDoc):
    collectorWorkset = EwrQcUtils.WorksetCheck(openedDoc)
    EwrQcUtils.ExcelWriter(excelFile, 'WORKSETS', 1, 0, collectorWorkset)
# Transaction
if len(collectorFiles) > 0:
    t = Transaction(doc, 'Check QAQC Elements')
    t.Start()
    for aDoc in collectorFiles:
        openedDoc = OpenFiles(aDoc, application, audit = False)
        print(str(openedDoc.Title) + ' Opened')
        workshareOp = WorksharingSaveAsOptions()
        # Define the name and location of excel file
        rawTitle = re.split('detached', openedDoc.Title)[0]
        title = rawTitle[0:len(rawTitle) -1]
        fileName = destinationFolder +'\\' + title + '.xlsx'
        # Define and Open Excel File
        excelFile = EwrQcUtils.ExcelOpener(fileName)
        # Create a blank intro Sheet
        blank =[]
        EwrQcUtils.ExcelWriter(excelFile, 'INTRO', 1, 0, blank)
        # Checking
        threading.Thread(name='DimensionsCheck', target = DimensionProcessing(openedDoc))
        threading.Thread(name='SettingsCheck', target=SettingsProcessing(openedDoc))
        threading.Thread(name='ViewssCheck', target=ViewsProcessing(openedDoc))
        threading.Thread(name='FamiliesCheck', target=FamiliesProcessing(openedDoc))
        threading.Thread(name='LinksCheck', target=LinksProcessing(openedDoc))
        threading.Thread(name='TitleBlockCheck', target=TitleBlocksProcessing(openedDoc))
        threading.Thread(name='SheetsCheck', target=SheetsProcessing(openedDoc))
        threading.Thread(name='TextsCheck', target=TextsProcessing(openedDoc))
        threading.Thread(name='PositionsCheck', target=PositionProcessing(openedDoc))
        threading.Thread(name='CateinWorksetsCheck', target=CateinWorksetsProcessing(openedDoc))
        threading.Thread(name='LevelssCheck', target=LevelsProcessing(openedDoc))
        threading.Thread(name='SheetElementsCheck', target=SheetElementsProcessing(openedDoc))
        threading.Thread(name='LinesCheck', target=LinesProcessing(openedDoc))
        threading.Thread(name='FilledRegionsCheck', target=FilledRegionsProcessing(openedDoc))
        threading.Thread(name='AnnotationsCheck', target=AnnotationsProcessing(openedDoc))
        threading.Thread(name='CadImportCheck', target=CadImportsProcessing(openedDoc))
        threading.Thread(name='WorksetsCheck', target=WorksetsProcessing(openedDoc))

        # Close Excel and Revit File
        excelFile.close()
        openedDoc.Close(False)
        print('File Saved' + fileName)

    # EwrQaUtils.FormattingLine(wb['LINE'])
    t.Commit()

else:
    forms.alert('No File is selected', title='', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)