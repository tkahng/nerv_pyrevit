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
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.DB import *
from Autodesk.Revit.ApplicationServices import Application
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')

__doc__ = 'Check whether certain view(s) from files at a specific location exist or not.' \

# models = r"\\uspadgv1dcl01\\NY BIM GROUP\\Projects\\3019262 (EWR T1)\\Models Sync\\NWC Export\\"
models = r"C:\\Users\\loum\\Desktop\\File Dump\\"
files = []
for file in os.listdir(models):
    if file.endswith(".rvt"):
        #print(str(file))
        files.append(str(file))
counter = 0
worksetList = []
outLst = []
checkName = 'NWC EXPORT STV'
# Open Files
for oFile in files:
    viewNames = []
    openOpt = OpenOptions()
    openOpt.Audit = False
    openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    wsopt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
    # wsopt.Open(worksetList)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(models + oFile)
    __revit__.OpenAndActivateDocument(modelPath, openOpt, False)
    try:
        DialogBoxShowingEventArgs.OverrideResult(1)
    except:
        pass
    # Define doc
    uidoc = __revit__.ActiveUIDocument
    doc = __revit__.ActiveUIDocument.Document
    placeholderfile  = "C:\\Users\\loum\\Desktop\\Empty Project.rvt"

    elements = DB.FilteredElementCollector(doc) \
        .OfCategory(BuiltInCategory.OST_Views) \
        .ToElements()
    for element in elements:
        try:
            viewName = element.LookupParameter('View Name').AsString()
        except:
            viewName = 'Error'
        viewNames.append(viewName)
    print(files[counter])
    if checkName in viewNames:
        print('View Exists')
    else:
        print('View does not Exist')
    docPlaceholder = __revit__.OpenAndActivateDocument(placeholderfile)
    doc.Close(False)
    counter += 1

