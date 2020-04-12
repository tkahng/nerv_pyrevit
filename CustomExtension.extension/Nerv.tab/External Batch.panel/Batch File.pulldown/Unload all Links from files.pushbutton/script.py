from pyrevit.framework import List
from pyrevit import revit, DB
import clr
import os
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
models = r"\\uspadgv1dcl01\\NY BIM GROUP\\Projects\\3019262 (EWR T1)\\Models Sync\\NWC Export\\"
files = []
for file in os.listdir(models):
    if file.endswith(".rvt"):
        print(str(file))
        files.append(str(file))
counter = 0
worksetList = []

__doc__ = 'Open projects and remove all the links.' \
          'Please do not use lightly'

# Open Files
for oFile in files:
    openOpt = OpenOptions()
    openOpt.Audit = False
    openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    wsopt = WorksetConfiguration(WorksetConfigurationOption.OpenLastViewed)
    wsopt.Open(worksetList)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(models + oFile)
    __revit__.OpenAndActivateDocument(modelPath, openOpt, False)
    # Define doc
    uidoc = __revit__.ActiveUIDocument
    doc = __revit__.ActiveUIDocument.Document
    placeholderfile  = "C:\\Users\\loum\\Desktop\\Empty Project.rvt"

    selection = [doc.GetElement(id)
            for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]

    t = Transaction(doc, 'Delete CAD Elements')
    # Get Fist View Position
    t.Start()

    RvtLinkObj = FilteredElementCollector(doc).OfClass(clr.GetClrType(RevitLinkType)).ToElements()

    for i in RvtLinkObj:
        rvtId = i.Id
        doc.Delete(rvtId)


    CadLinkObj = FilteredElementCollector(doc).OfClass(clr.GetClrType(ImportInstance)).ToElements()

    for a in CadLinkObj:
	    CadId = a.Id
	    doc.Delete(CadId)

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
