import sys
import ConfigParser
from os.path import expanduser
import csv
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
    ViewFamily, View3D, IndependentTag, ElementId, StorageType
from System.Collections.Generic import List
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application
clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')
# Collect Save location and Rvt Files
def Importcsv(Filename):
    flat_list = []
    with open(Filename, 'r') as f:
        reader = csv.reader(f)
        Lst = list(reader)
        for sublist in Lst:
            flat_list.append(sublist)
            #for item in sublist:
                #flat_list.append(item)
    return flat_list

class ChangeElement:
    def ChangeParameter(self, id, parameter, value):
        self.Id = id
        self.Parameter = parameter
        self.Value = value
        return self

def OpenFiles(oFile, app, audit):
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
    return currentdoc


collectorCSVFile = forms.pick_file(file_ext='csv', multi_file=False, unc_paths=False)
collectorFiles = forms.pick_file(file_ext='rvt', multi_file=True, unc_paths=False)
destinationFolder = forms.pick_folder()
# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Extract information from csv file and batch apply parameter value changes.'\
          'Format of csv: "model name, element Id, parameter name, new parameter value".'\
            'Step 1: Select the csv File'\
            'Step 2: Select the Revit Files'\
            'Step 3: Select the directory new models to be placed.'
uiapp = UIApplication(doc.Application)
application = uiapp.Application

if len(collectorFiles) > 0:
    for aDoc in collectorFiles:
        openedDoc = OpenFiles(aDoc, application, audit=False)
        t = Transaction(openedDoc, "Apply Parameters")
        t.Start()
        print(str(openedDoc.Title) + ' Opened')
        workshareOp = WorksharingSaveAsOptions()
        # Define the name and location of excel file
        rawTitle = re.split('detached', openedDoc.Title)[0]
        title = rawTitle[0:len(rawTitle) -1]
        print(str(title) + ' is being modified:')
        for line in Importcsv(collectorCSVFile):
            modelName = line[0]
            id = line[1]
            parameterName = line[2]
            parameterValue = line[3]
            v1 = ()
            if modelName == title:
                element = ()
                try:
                    element = openedDoc.GetElement(ElementId(int(id)))
                except:
                    print("ElementId {0} Does not Exist".format(str(id)))
                try:
                    v1 = element.LookupParameter(parameterName)
                except:
                    print("Error finding the value to {0} for {1}".format(parameterName, str(id)))
                if v1:
                    if v1.StorageType == StorageType.Integer:
                        try:
                            element.LookupParameter(parameterName).Set(int(parameterValue))
                            print("Applied change {0} as {1}".format(id, parameterValue))
                        except:
                            print("Error Applying the value to {0} ".format(str(id)) + parameterName + " as integer")
                    elif v1.StorageType == StorageType.String:
                        try:
                            element.LookupParameter(parameterName).Set(str(parameterValue))
                            print("Applied change {0} as {1}".format(id, parameterValue))
                        except:
                            print("Error Applying the value to {0} ".format(str(id)) + parameterName + " as string")
                    elif v1.StorageType == StorageType.Double:
                        try:
                            element.LookupParameter(parameterName).Set(float(parameterValue))
                            print("Applied change {0} as {1}".format(id, parameterValue))
                        except:
                            print("Error Applying the value to {0} ".format(str(id)) + parameterName + " as double")
                    else:
                        print("Error Applying the value to {0} ".format(str(id)) + parameterName + " format error")

        t.Commit()
        saveOp = SaveAsOptions()
        workOp = WorksharingSaveAsOptions()
        workOp.SaveAsCentral = True
        saveOp.SetWorksharingOptions(workOp)
        saveAsTitle = openedDoc.Title
        openedDoc.SaveAs(destinationFolder + '\\' + saveAsTitle, saveOp)
        openedDoc.Close(False)
        print("--------------------------")
