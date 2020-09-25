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
    ViewFamily, View3D, TextElement, BuiltInParameter, IndependentTag, ViewSheet
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
    wsopt = WorksetConfiguration(WorksetConfigurationOption.OpenAllWorksets)
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
#process = ["HVAC Models", "Other Models"]
#pickedProcess = forms.SelectFromList.show(process, button_name='Select Item', multiselect=False)

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
        sheets = FilteredElementCollector(openedDoc).OfClass(ViewSheet).ToElements()
        viewSheetDict = {}
	print(openedDoc.Title)
        collectorEAMElements = [['Model Name', 'Format', 'EAM_11_UAID', 'TagID', 'hostID', 'View', 'Sheet']]
        for viewSheet in sheets:
            sheetNumber = viewSheet.SheetNumber
            views = viewSheet.GetAllPlacedViews()
            viewList = []
            for view in views:
            	#    viewList.append(view)
            	#for v in viewList:
                #viewSheetDict[openedDoc.GetElement(view).Title] = sheetNumber
        	#print(viewSheetDict.keys())
                tags = FilteredElementCollector(openedDoc, view).OfClass(IndependentTag).ToElements()#.WherePasses(catFilter).WherePasses(idFilter)
		        #print(len(tags))
                texts = FilteredElementCollector(openedDoc, view).OfClass(TextElement).ToElements()
                sheetTexts = FilteredElementCollector(openedDoc, viewSheet.Id).OfClass(TextElement).ToElements()
		        #print(len(texts))
                for text in texts:
                    line = []
                    #textWorkset = text.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
                    #textView = textWorkset[6:-1]
                    word = text.Text
                    #print(word)
                    if "AVIA_EWR" in word:
                    #print("Text True")
                        items = word.split('AVIA_EWR')
                        for item in items[1:]:
                            uaid = 'AVIA_EWR' + item
                            try:
                                id = text.Id.IntegerValue
                            except:
                                id = ""
                            line = [title, 'TEXT', uaid, id, ' ', openedDoc.GetElement(view).Title, sheetNumber]
                            collectorEAMElements.append(line)
                for sheetText in sheetTexts:
                    sheetLine = []
                    # textWorkset = text.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
                    # textView = textWorkset[6:-1]
                    sheetWord = sheetText.Text
                    # print(word)
                    if "AVIA_EWR" in sheetWord:
                        # print("Text True")
                        sheetItems = sheetWord.split('AVIA_EWR')
                        for sheetItem in sheetItems[1:]:
                            sheetUaid = 'AVIA_EWR' + sheetItem
                            try:
                                id = sheetText.Id.IntegerValue
                            except:
                                id = ""
                            sheetLine = [title, 'TEXT', sheetUaid, id, ' ', openedDoc.GetElement(view).Title,
                                    sheetNumber]
                            collectorEAMElements.append(sheetLine)
			    #print(len(collectorEAMElements))
                for tag in tags:
                    #workset = tag.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
                    #view = workset[6:-1].split(": ")[1]
                    #view = workset[6:-1]
                    #print(view)
                    try:
                        tagtext = tag.TagText
                    except:
                        tagtext = ""
                    multi = tag.IsMulticategoryTag
                    #print(tagtext)
                    if "AVIA_EWR" in tagtext and multi:
			            #print("Tag True")
                        try:
                            id = tag.Id.IntegerValue
                        except:
                            id = ""
                        try:
                            hostId = tag.TaggedElementId.HostElementId.IntegerValue
                        except:
                            hostId = ""
                        tagline = [title, 'TAG', tagtext, id, hostId, openedDoc.GetElement(view).Title, sheetNumber]
                        collectorEAMElements.append(tagline)
			#print(len(collectorEAMElements))
        EAMQcUtils.ExcelWriter(excelFile, 'ID', 0, 0, collectorEAMElements)
        t.Commit()

        # Close Excel and Revit File
        excelFile.close()
        openedDoc.Close(False)
        print('File Saved' + fileName)

    # WmataQcUtils.FormattingLine(wb['LINE'])


else:
    forms.alert('No File is selected', title='', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)