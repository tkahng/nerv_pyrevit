import os
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
	OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,\
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, FBXExportOptions, View
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs

def RVTFileCollector(dir):
    files = []
    for file in os.listdir(dir):
        if file.endswith(".rvt"):
            #print(str(file))
            files.append(str(file))
    print files
    return files

def OpenFile(oFile, app, audit):
    openOpt = OpenOptions()
    if audit == True:
        openOpt.Audit = True
    else:
        openOpt.Audit = False
    openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    wsopt = WorksetConfiguration(WorksetConfigurationOption.OpenAllWorksets)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(oFile)
    currentdoc = app.OpenDocumentFile(modelPath, openOpt)
    try:
        DialogBoxShowingEventArgs.OverrideResult(1)
    except:
        pass
    return currentdoc

def OpenFileCloseWorksets(oFile, app, audit):
    openOpt = OpenOptions()
    if audit == True:
        openOpt.Audit = True
    else:
        openOpt.Audit = False
    openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    wsopt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(oFile)
    currentdoc = app.OpenDocumentFile(modelPath, openOpt)
    try:
        DialogBoxShowingEventArgs.OverrideResult(1)
    except:
        pass
    return currentdoc


def ExportFBX(Document, View, Location):
    FBXop = FBXExportOptions()
    FBXop.StopOnError = False
    name = Document.Title
    Document.Export(Location, name, View, FBXop)

def GetViewByName(Document, ViewName):
    viewCollector = FilteredElementCollector(Document). OfClass(View)
    for i in viewCollector:
        if ViewName in i.Title:
            return i
