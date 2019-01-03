
import clr
import os
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector,CADLinkType, Transaction, ImportInstance, \
	OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,ModelPathUtils
from Autodesk.Revit.DB import BuiltInCategory, ElementId, ExternalFileReference, RevitLinkType,ISaveSharedCoordinatesCallback
from System.Collections.Generic import List
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
# models = r"\\uspadgv1dcl01\\NY BIM GROUP\\Projects\\3019262 (EWR T1)\\Models Sync\\NWC Export\\"
# File Collector
models = r"C:\\Users\\loum\\Desktop\\File Dump\\"
def RVTFileCollector(dir):
    files = []
    for file in os.listdir(dir):
        if file.endswith(".rvt"):
            #print(str(file))
            files.append(str(file))
    print files
    return files

def OpenFiles(files,app):
    counter = 0
    worksetList = []
    outLst = []
    checkName = 'NWC EXPORT STV'
    for oFile in files:
        viewNames = []
        openOpt = OpenOptions()
        openOpt.Audit = False
        openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
        wsopt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
        # wsopt.Open(worksetList)
        openOpt.SetOpenWorksetsConfiguration(wsopt)
        modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(models + oFile)
        # doc = Application.OpenDocumentFile(modelPath, openOpt)
        doc = app.OpenDocumentFile(modelPath, openOpt)
        try:
            DialogBoxShowingEventArgs.OverrideResult(1)
        except:
            pass
        print(str(doc) +' Opened')
        counter += 1

# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selection = [doc.GetElement(id) for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
__doc__ = 'Open projects and remove all the links '\
            'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Transaction
t = Transaction(doc, 'Delete Excess Sheets Elements')
t.Start()
allFiles = RVTFileCollector(models)
OpenFiles(allFiles, application)
t.Commit()