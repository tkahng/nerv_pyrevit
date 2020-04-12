from pyrevit.framework import List
from pyrevit import revit, DB, forms

import clr
import os
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
	OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions

from System.Collections.Generic import List
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')

# File Collector
# models = r"C:\\Users\\loum\\Desktop\\File Dump\\"

collectorFiles = forms.pick_file(file_ext='rvt', multi_file=True, unc_paths=False)
desiinationFolder = forms.pick_folder(title='SaveTo.....')
def RVTFileCollector(dir):
    files = []
    for file in os.listdir(dir):
        if file.endswith(".rvt"):
            #print(str(file))
            files.append(str(file))
    print files
    return files

def OpenFiles(files, app, audit):
    counter = 0
    for oFile in files:
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
        # doc = Application.OpenDocumentFile(modelPath, openOpt)
        docs = []
        currentdoc = app.OpenDocumentFile(modelPath, openOpt)
        try:
            DialogBoxShowingEventArgs.OverrideResult(1)
        except:
            pass
        print(str(doc) +' Opened')
        counter += 1
        docs.append(currentdoc)
    return docs


# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Open projects and resave in a specific location'\
            'Please do not use lightly'

uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Transaction
if len(collectorFiles) > 0:
    t = Transaction(doc, 'Delete Excess Sheets Elements')
    t.Start()
    # allFiles = RVTFileCollector(collectorFiles)
    openedDoc = OpenFiles(collectorFiles, application, audit = True)
    saveOp = SaveAsOptions()
    workshareOp = WorksharingSaveAsOptions()
    workshareOp.SaveAsCentral = True
    saveOp.SetWorksharingOptions(workshareOp)
    count = 0
    print(len(openedDoc))
    for file in openedDoc:
        file.SaveAs(desiinationFolder + '\\' + file.Title, saveOp)
        file.Close(False)
        count += 1
    t.Commit()
else:
    forms.alert('No File is selected', title='', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)