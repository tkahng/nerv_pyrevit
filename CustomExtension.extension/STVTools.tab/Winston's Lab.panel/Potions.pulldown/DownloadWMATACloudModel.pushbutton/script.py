
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

import System, Selection
import System.Threading
import System.Threading.Tasks
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, Family,Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, SpatialElementTag, RevitLinkInstance, RevitLinkType, \
    OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,\
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions
import re
from Autodesk.Revit.DB import Level, BuiltInParameter
from Autodesk.Revit.UI import TaskDialog, UIApplication
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReferenceByPartialName('System')
import System
from System import Guid
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs

uiapp = UIApplication(doc.Application)
application = uiapp.Application

def OpenCloudFiles(modelGUID, projectGUID, app, audit):
    openOpt = OpenOptions()
    if audit == True:
        openOpt.Audit = True
    else:
        openOpt.Audit = False
    # openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    wsopt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
    # wsopt.Open(worksetList)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertCloudGUIDsToCloudPath(projectGUID, modelGUID)
    currentdoc = app.OpenDocumentFile(modelPath, openOpt)
    try:
        DialogBoxShowingEventArgs.OverrideResult(1)
    except:
        pass
    return currentdoc

def SaveCloudModel(document, filePath):
    worksharingOptions = WorksharingSaveAsOptions()
    worksharingOptions.SaveAsCentral = True
    saveOpt = SaveAsOptions()
    saveOpt.SetWorksharingOptions(worksharingOptions)
    saveOpt.OverwriteExistingFile = True
    saveOpt.Compact = True
    document.SaveAs(filePath + document.Title + ".rvt", saveOpt)
    document.Close()

filePath = "\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\4020310\\4020310_0001\\90_CAD Models and Sheets\\07_A_Architectural\\"
modelGUID = Guid("e77aa560-8776-4a0e-8192-3044c5e240df")
projectGUID = Guid("20ac335a-5ba8-4520-b948-296e529c3306")
versionName = application.VersionName
if versionName == "Autodesk Revit 2020":
    openedDoc = OpenCloudFiles(modelGUID, projectGUID, application, audit=False)
    SaveCloudModel(openedDoc, filePath)
    print("Download Complete")
else:
    print("Please open revit 2020 and retry")
