from pyrevit.framework import List
from pyrevit import revit, DB
import clr
import os
from pyrevit import forms
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector,CADLinkType, Transaction, ImportInstance, \
	OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,ModelPathUtils
from Autodesk.Revit.DB import BuiltInCategory, ElementId, ExternalFileReference, RevitLinkType,ISaveSharedCoordinatesCallback
from System.Collections.Generic import List
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.DB import *
from Autodesk.Revit.ApplicationServices import Application
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')

__doc__ = 'Delete Excess Sheet(s) from files.'

# Model Path and file path
# models = r"\\uspadgv1dcl01\\NY BIM GROUP\\Projects\\3019262 (EWR T1)\\Models Sync\\NWC Export\\"
# models = r'C:\Users\loum\Desktop\File Dump\\'
placeholderfile  = "C:\\Users\\loum\\Desktop\\Empty Project.rvt"
models = forms.pick_folder()
# File collectors
files = []
for file in os.listdir(models):
    if file.endswith(".rvt"):
        print(str(file))
        files.append(str(file))
counter = 0
worksetList = []

# Open Files
for oFile in files:
    print(models + oFile)
    openOpt = OpenOptions()
    openOpt.Audit = False
    openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    wsopt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
    wsopt.Open(worksetList)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(str(models) + '\\' + oFile)
    modelString = models + oFile
    # Application.OpenDocumentFile(modelPath, openOpt)
    __revit__.OpenAndActivateDocument(modelPath, openOpt, False)
    # Define doc
    uidoc = __revit__.ActiveUIDocument
    doc = __revit__.ActiveUIDocument.Document
    selection = [doc.GetElement(id)
            for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    
    t = Transaction(doc, 'Delete Excess Sheets Elements')
    # Get Fist View Position
    t.Start()
# TODO: CHECK WHAT HAPPENED TO THIS
    RvtSheetObj = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()

    for i in RvtSheetObj:
        rvtId = i.Id
        doc.Delete(rvtId)

    t.Commit()

# Resave as Central
    name = files[counter]
    opt = SaveAsOptions()
    opt.OverwriteExistingFile = True
    opt.Compact = True
    wsopt = WorksharingSaveAsOptions()
    wsopt.ClearTransmitted = False
    wsopt.SaveAsCentral = True
    opt.SetWorksharingOptions(wsopt)
    doc.SaveAs(models + name, opt)
    docPlaceholder = __revit__.OpenAndActivateDocument(placeholderfile)
    doc.Close(False)
    counter += 1
