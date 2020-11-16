
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
import Selection
clr.AddReference('System')
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory,\
    RevitLinkInstance, UV, XYZ, SpatialElementBoundaryOptions, CurveArray, ElementId, View, RevitLinkType, WorksetTable,\
    Workset, FilteredWorksetCollector, WorksetKind, RevitLinkType, RevitLinkInstance

from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document




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
    ViewFamily, View3D, IndependentTag
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
    wsopt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
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

eleIdDic = {
    "12114958": "A16007000-3D_CENTRAL", "11962259": "A16007000-3D_CENTRAL", "12114971": "A16007000-3D_CENTRAL", "11967658": "A16007000-3D_CENTRAL", "12114946": "A16007000-3D_CENTRAL", "11967134": "A16007000-3D_CENTRAL", "2731309": "M17017000-FP_CENTRAL", "7763086": "M17017000-FP_CENTRAL", "6341723": "M17017000-FP_CENTRAL", "7394149": "M17017000-FP_CENTRAL", "6188415": "M17017000-FP_CENTRAL", "7394457": "M17017000-FP_CENTRAL", "39531502": "A17017000-3D_CENTRAL", "69055286": "A17017000-3D_CENTRAL", "68119330": "A17017000-3D_CENTRAL", "39531501": "A17017000-3D_CENTRAL", "71542658": "A17017000-3D_CENTRAL", "71542648": "A17017000-3D_CENTRAL", "39552085": "A17017000-3D_CENTRAL", "69075198": "A17017000-3D_CENTRAL", "61978516": "A17017000-3D_CENTRAL", "39432793": "A17017000-3D_CENTRAL", "72695471": "A17017000-3D_CENTRAL", "72373583": "A17017000-3D_CENTRAL", "70907157": "A17017000-3D_CENTRAL", "42796098": "A17017000-3D_CENTRAL", "72695524": "A17017000-3D_CENTRAL", "72373564": "A17017000-3D_CENTRAL", "70907101": "A17017000-3D_CENTRAL", "55557959": "A17017000-3D_CENTRAL", "91375480": "A17017000-3D_CENTRAL", "87964369": "A17017000-3D_CENTRAL", "55557960": "A17017000-3D_CENTRAL", "91375462": "A17017000-3D_CENTRAL", "87964389": "A17017000-3D_CENTRAL", "2094119": "M17017000-FP_CENTRAL", "7688458": "M17017000-FP_CENTRAL", "6817694": "M17017000-FP_CENTRAL", "7669500": "M17017000-FP_CENTRAL", "6817852": "M17017000-FP_CENTRAL", "7669506": "M17017000-FP_CENTRAL", "6198846": "M17017000-FP_CENTRAL", "7856208": "M17017000-FP_CENTRAL", "4597206": "M17017000-FP_CENTRAL", "7669574": "M17017000-FP_CENTRAL", "1724294": "M17017000-FP_CENTRAL", "7745633": "M17017000-FP_CENTRAL", "6296234": "M17017000-FP_CENTRAL", "7799917": "M17017000-FP_CENTRAL", "6069415": "M17017000-BH_CENTRAL", "6069413": "M17017000-BH_CENTRAL", "6069363": "M17017000-BH_CENTRAL", "6069361": "M17017000-BH_CENTRAL", "6069432": "M17017000-BH_CENTRAL", "6069430": "M17017000-BH_CENTRAL", "6069449": "M17017000-BH_CENTRAL", "6069447": "M17017000-BH_CENTRAL", "6069298": "M17017000-BH_CENTRAL", "6069273": "M17017000-BH_CENTRAL", "6069327": "M17017000-BH_CENTRAL", "6069325": "M17017000-BH_CENTRAL", "5836928": "M17017000-FP_CENTRAL", "7795450": "M17017000-FP_CENTRAL", "51566744": "A17017000-3D_CENTRAL", "72891006": "A17017000-3D_CENTRAL", "67911548": "A17017000-3D_CENTRAL", "50940925": "A17017000-3D_CENTRAL", "72801526": "A17017000-3D_CENTRAL", "72020932": "A17017000-3D_CENTRAL", "67217650": "A17017000-3D_CENTRAL", "91402124": "A17017000-3D_CENTRAL", "102452898": "A17017000-3D_CENTRAL", "6622484": "M17017000-FP_CENTRAL", "7800305": "M17017000-FP_CENTRAL", "3410461": "M17017000-FP_CENTRAL", "7754226": "M17017000-FP_CENTRAL", "3611268": "M17017000-3D_CENTRAL_GEN", "1178243": "M17017000-3D_CENTRAL_GEN", "2803733": "M17017000-3D_CENTRAL_GEN", "3441939": "E17017000-3D_CENTRAL_GEN", "4108319": "E17017000-3D_CENTRAL_GEN", "877238": "M17017000-3D_CENTRAL_GEN", "1078358": "M17017000-3D_CENTRAL_GEN", "979510": "M17017000-3D_CENTRAL_GEN", "4108318": "E17017000-3D_CENTRAL_GEN", "1079027": "M17017000-3D_CENTRAL_GEN", "987535": "M17017000-3D_CENTRAL_GEN", "4103096": "E17017000-3D_CENTRAL_GEN", "1079046": "M17017000-3D_CENTRAL_GEN", "4791744": "E17017000-3D_CENTRAL_GEN", "4096678": "E17017000-ES_CENTRAL_GEN_C", "4791780": "E17017000-3D_CENTRAL_GEN", "4096856": "E17017000-ES_CENTRAL_GEN_C", "3102590": "M17017000-3D_CENTRAL_GEN", "3181601": "M17017000-3D_CENTRAL_GEN"}

__doc__ = 'Report the selected Model Element Quality Check outcome in an Excel file.'\
          'Open projects and resave in a specific location.'\
            'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application

collectorEAMElements = [['Model Name', 'Categoty', 'ElementID', 'Family', 'Type', 'X', 'Y', 'Z']]
fileName = destinationFolder + "\\" + "Export File" + '.xlsx'
excelFile = EAMQcUtils.ExcelOpener(fileName)

if len(collectorFiles) > 0:
    for aDoc in collectorFiles:
        openedDoc = OpenFiles(aDoc, application, audit=False)
        t = Transaction(openedDoc, 'Check QAQC Elements')
        print(str(openedDoc.Title) + ' Opened')
        workshareOp = WorksharingSaveAsOptions()
        # Define the name and location of excel file
        rawTitle = re.split('detached', openedDoc.Title)[0]
        title = rawTitle[0:len(rawTitle) -1]

        # Create a blank intro Sheet
        blank =[]
        # EAMQcUtils.ExcelWriter(excelFile, 'INTRO', 1, 0, blank)
        elements = []
        for ele in eleIdDic.keys():
            keywords = eleIdDic[ele].split("_")
            switch = True
            for keyword in keywords:
                if not keyword in openedDoc.Title:
                    switch = False
            if switch:
                print(int(ele))
                elements.append(openedDoc.GetElement(ElementId(int(ele))))
        for ele in elements:
            try:
                cate = ele.Category.Name
            except:
                cate = ""
            try:
                id = ele.Id.ToString()
            except:
                id = ""
            if id:
                try:
                    family = openedDoc.GetElement(ele.LookupParameter('Family').AsElementId()).FamilyName
                except:
                    family = ""
                    # Get Type
                try:
                    type = openedDoc.GetElement(ele.LookupParameter('Type').AsElementId()).LookupParameter('Type Name').AsString()
                    # print(type)
                except:
                    type = ""
                    # Get Location

                loc = ele.Location
                try:
                    try:
                        point = loc.Point
                        X = point.X
                        Y = point.Y
                        Z = point.Z
                        # print("point")
                    except:
                        startPoint = loc.Curve.GetEndPoint(0)
                        endPoint = loc.Curve.GetEndPoint(1)
                        X = (startPoint.X + endPoint.X) / 2
                        Y = (startPoint.Y + endPoint.Y) / 2
                        Z = (startPoint.Z + endPoint.Z) / 2
                        # print("curve")
                except:
                    X = ""
                    Y = ""
                    Z = ""
                    # print("None")

                line = [title, cate, id, family, type, X, Y, Z]
                collectorEAMElements.append(line)
        # EAMQcUtils.ExcelWriter(excelFile, 'ELEMENTS', 0, 0, collectorEAMElements)
        # excelFile.close()
        # Close Excel and Revit File

        openedDoc.Close(False)
        print('File Saved' + fileName)

    # WmataQcUtils.FormattingLine(wb['LINE'])


else:
    forms.alert('No File is selected', title='', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)

EAMQcUtils.ExcelWriter(excelFile, 'ELEMENTS', 0, 0, collectorEAMElements)
excelFile.close()