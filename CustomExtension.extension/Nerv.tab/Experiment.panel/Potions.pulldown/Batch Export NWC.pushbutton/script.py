import sys, re
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
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, RevitLinkType, ViewSet,WorksharingSaveAsOptions, NavisworksExportOptions
from System.Collections.Generic import List
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application

# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Open projects and export NWC'\
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
    cleanTitle = re.split('_detached', title)[0]
    print(cleanTitle)
    currentDoc.SaveAs(destinationFolder + '\\' + title, saveOp)
    currentDoc.Close(False)
    # Open again
    currentDoc2 = FileUtilities.OpenFile(destinationFolder + '\\' + title, application, False)
    try:
        try:
            view = FileUtilities.GetViewByName(currentDoc2, "3D-NWC EXPORT STV").Id
        except:
            view = FileUtilities.GetViewByName(currentDoc2, "NWC EXPORT STV").Id
        element = FilteredElementCollector(currentDoc2, view).ToElementIds()
        nwcOptions = NavisworksExportOptions()
        nwcOptions.SetSelectedElementIds(element)
        currentDoc2.Export(destinationFolder, cleanTitle, nwcOptions)
        currentDoc2.Close(False)
    except:
        print('No proper View Found in the ' + cleanTitle)
        currentDoc2.Close(False)


