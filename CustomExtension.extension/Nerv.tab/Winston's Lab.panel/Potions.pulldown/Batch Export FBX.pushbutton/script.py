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

import FileUtilities, Selection
from pyrevit.framework import List
from pyrevit import revit, DB, forms
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
	OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,\
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, RevitLinkType, ViewSet,WorksharingSaveAsOptions
from System.Collections.Generic import List
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application

# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Open projects and export FBX'\
            'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Collect Save location and Rvt Files
collectorFiles = forms.pick_file(file_ext='rvt', multi_file=True, unc_paths=False)
destinationFolder = forms.pick_folder()

# open File and export
for f in collectorFiles:
    currentDoc = FileUtilities.OpenFileCloseWorksets(f, application, False)
    # Unload Links
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
    title = currentDoc.Title
    currentDoc.SaveAs(destinationFolder + '\\' + title, saveOp)
    currentDoc.Close(False)
    # Open again
    currentDoc2 = FileUtilities.OpenFile(destinationFolder + '\\' + title, application, False)
    view = FileUtilities.GetViewByName(currentDoc2, "FBX Export")
    set = ViewSet()
    set.Insert(view)
    FileUtilities.ExportFBX(currentDoc2, set, destinationFolder)
    currentDoc2.Close(False)



