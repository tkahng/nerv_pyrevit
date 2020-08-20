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
import EAMQcUtils
import xlsxwriter
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
	OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,\
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, RevitLinkType, ViewFamilyType, \
    ViewFamily, View3D, IndependentTag
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
    wsopt = WorksetConfiguration(WorksetConfigurationOption.OpenAllWorksets)
    # wsopt.Open(worksetList)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(oFile)
    currentdoc = app.OpenDocumentFile(modelPath, openOpt)
    try:
        DialogBoxShowingEventArgs.OverrideResult(1)
    except:
        pass
    return currentdoc

def OpenFilesandUnload(oFile, app, audit):
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
    revitLinkType = FilteredElementCollector(doc).OfClass(RevitLinkType).ToElements()
    for r in revitLinkType:
        try:
            r.Unload(None)
        except:
            pass
    saveOp = SaveAsOptions()
    workOp = WorksharingSaveAsOptions()
    workOp.SaveAsCentral = True
    saveOp.SetWorksharingOptions(workOp)
    title = currentdoc.Title
    currentdoc.SaveAs(destinationFolder + '\\' + title, saveOp)
    currentdoc.Close(False)
# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Report the selected Model Element Quality Check outcome in an Excel file.'\
          'Open projects and resave in a specific location.'\
            'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Pick an action
process = ["HVAC Models", "Other Models"]
pickedProcess = forms.SelectFromList.show(process, button_name='Select Item', multiselect=False)

if len(collectorFiles) > 0:
    for aDoc in collectorFiles:

        openedDoc = OpenFiles(aDoc, application, audit=False)
        t = Transaction(openedDoc, 'Check QAQC Elements')
        t.Start()
        print(str(openedDoc.Title) + ' Opened')
        workshareOp = WorksharingSaveAsOptions()
        # Define the name and location of excel file
        rawTitle = re.split('detached', openedDoc.Title)[0]
        title = rawTitle[0:len(rawTitle) -1]
        fileName = destinationFolder +'\\' + title + '.xlsx'
        # Define and Open Excel File
        excelFile = EAMQcUtils.ExcelOpener(fileName)
        # Create a blank intro Sheet
        blank =[]
        # EAMQcUtils.ExcelWriter(excelFile, 'INTRO', 1, 0, blank)
        # Create View

        threeDViews = []

        viewFamilyTypes = FilteredElementCollector(openedDoc).OfClass(ViewFamilyType).ToElements()
        for viewFa in viewFamilyTypes:
            if viewFa.ViewFamily == ViewFamily.ThreeDimensional:
                threeDViews.append(viewFa.Id)
        # viewTypeId =  ViewType.ThreeD.Id
        view = View3D.CreateIsometric(openedDoc, threeDViews[0])

        view.ViewName = "EAM View"
        # Checking
        #catFilter =
        #idFilter =
        if pickedProcess == "Other Models":
            collectorEAMElements = [['Model Name', 'Categoty', 'ElementID', 'EAM_11_UAID', 'EAM_EID', 'UAID_Required', 'Sheet', 'New EAM_11_UAID']]
            elements = FilteredElementCollector(openedDoc, view.Id).WhereElementIsNotElementType().ToElements()#.WherePasses(catFilter).WherePasses(idFilter)
            for ele in elements:
                try:
                    cate = ele.Category.Name
                except:
                    cate = ""
                id = ele.Id.ToString()
                try:
                    EAM_11_UAID = ele.LookupParameter('EAM_11_UAID').AsString()
                except:
                    EAM_11_UAID = ""
                try:
                    EAM_EID = ele.LookupParameter('EAM_EID').AsString()
                except:
                    EAM_EID = ""
                try:
                    UAID_Required = ele.LookupParameter('UAID_Required').AsString()
                except:
                    UAID_Required = ""
                line = [title, cate, id, EAM_11_UAID, EAM_EID, UAID_Required]
                collectorEAMElements.append(line)
            EAMQcUtils.ExcelWriter(excelFile, 'ELEMENTS', 0, 0, collectorEAMElements)
        elif pickedProcess == "HVAC Models":
            collectorEAMElements = [['Model Name', 'Categoty', 'ElementID', 'EAM_11_UAID', 'EAM_12_COMPONENT_01',
                                     'EAM_12_COMPONENT_02', 'EAM_12_COMPONENT_03', 'EAM_12_COMPONENT_04',
                                     'EAM_12_COMPONENT_05', 'EAM_12_COMPONENT_06', 'EAM_12_COMPONENT_07',
                                     'EAM_12_COMPONENT_08', 'EAM_12_COMPONENT_09', 'EAM_12_COMPONENT_10',
                                     'EAM_12_COMPONENT_11', 'EAM_12_COMPONENT_12', 'EAM_12_COMPONENT_13',
                                     'EAM_12_COMPONENT_14', 'EAM_12_COMPONENT_15',
                                     'EAM_EID', 'UAID_Required', 'Sheet', 'New EAM_11_UAID']]
            paraList = ['EAM_11_UAID', 'EAM_12_COMPONENT_01',
                                     'EAM_12_COMPONENT_02', 'EAM_12_COMPONENT_03', 'EAM_12_COMPONENT_04',
                                     'EAM_12_COMPONENT_05', 'EAM_12_COMPONENT_06', 'EAM_12_COMPONENT_07',
                                     'EAM_12_COMPONENT_08', 'EAM_12_COMPONENT_09', 'EAM_12_COMPONENT_10',
                                     'EAM_12_COMPONENT_11', 'EAM_12_COMPONENT_12', 'EAM_12_COMPONENT_13',
                                     'EAM_12_COMPONENT_14', 'EAM_12_COMPONENT_15', 'EAM_EID', 'UAID_Required']
            elements = FilteredElementCollector(openedDoc).WhereElementIsNotElementType().ToElements()#.WherePasses(catFilter).WherePasses(idFilter)
            for ele in elements:
                try:
                    cate = ele.Category.Name
                except:
                    cate = ""
                id = ele.Id.ToString()
                line = [title, cate, id]
                for para in paraList:
                    try:
                        value = ele.LookupParameter(para).AsString()
                    except:
                        value = ""
                    line.append(value)
                collectorEAMElements.append(line)
            EAMQcUtils.ExcelWriter(excelFile, 'ELEMENTS', 0, 0, collectorEAMElements)
        t.Commit()

        # Close Excel and Revit File
        excelFile.close()
        openedDoc.Close(False)
        print('File Saved' + fileName)

    # WmataQcUtils.FormattingLine(wb['LINE'])


else:
    forms.alert('No File is selected', title='', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)