from pyrevit.framework import List
from pyrevit import revit, DB, forms
import re, clr, os, threading
import EAMQcUtils
import xlsxwriter

clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
    OpenOptions, WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, RevitLinkType, ViewFamilyType, \
    ViewFamily, View3D, IndependentTag, BuiltInParameter, FamilyType, BuiltInParameter
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
def get_pos_tag_parameters_as_list(element):
    '''
    Get a Dictionary of all element name, value and parameter object
    :param element:
    :return: dictionary
    '''
    parameters = element.Parameters
    _param = []
    for param in parameters:
        if param:
            name = param.Definition.Name
            value = ""
            if 'String' in str(param.StorageType):
                try:
                    value = str(param.AsString())
                    if value:
                        _param.append(name + ': ' + value)
                except:
                    value = str(param.AsValueString())
                    if value:
                        _param.append(name + ': '+ value)
            elif 'Interger' in str(param.StorageType):
                value = str(param.AsInterger())
                if value:
                    _param.append(name + ': ' + value)
    return _param

def RVTFileCollector(dir):
    files = []
    for file in os.listdir(dir):
        if file.endswith(".rvt"):
            # print(str(file))
            files.append(str(file))
    return files


def OpenFiles(oFile, app, audit):
    openOpt = OpenOptions()
    if audit == True:
        openOpt.Audit = True
    else:
        openOpt.Audit = False
    openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets

    # Needed for specific view to work:
    # wsopt = WorksetConfiguration(WorksetConfigurationOption.OpenAllWorksets)

    # Better for all elements as faster and unload all links cause worksets closed:
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


def get_parameters_as_dic(element):
    '''
    Get a Dictionary of all element name, value and parameter object
    :param element, paraName:
    :return:list
    '''
    parameters = element.Parameters
    _param = {}
    for param in parameters:
        if param:
            name = param.Definition.Name
            if 'String' in str(param.StorageType):
                try:
                    _param[name] = str(param.AsString())
                except:
                    _param[name] = str(param.AsValueString())
            elif 'Interger' in str(param.StorageType):
                _param[name] =str(param.AsInterger())
    return _param

# Not needed anymore
# First Line of the csv File
# elementTitle = [['Model Name', 'Categoty', 'ElementID', "Type Id" 'Mark']]
# typeTitle = [['Model Name', 'Categoty', 'ElementID',  'Type Mark']]
# List of Parameters


# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Report the selected Model Element Quality Check outcome in an Excel file.' \
          'Open projects and resave in a specific location.' \
          'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Pick an action, #view specific will create default 3d view with current visibility

if len(collectorFiles) > 0:
    for aDoc in collectorFiles:

        # Open Document
        openedDoc = OpenFiles(aDoc, application, audit=False)
        t = Transaction(openedDoc, 'Check QAQC Elements')
        t.Start()
        # Opening Settings and clean up
        print(str(openedDoc.Title) + ' Opened')
        workshareOp = WorksharingSaveAsOptions()
        # Define the name and location of excel file
        rawTitle = re.split('detached', openedDoc.Title)[0]
        title = rawTitle[0:len(rawTitle) - 1]
        fileName = destinationFolder + '\\' + title + '.xlsx'
        # Define and Open Excel File
        excelFile = EAMQcUtils.ExcelOpener(fileName)
        # Create a blank intro Sheet

        elements = FilteredElementCollector(openedDoc).WhereElementIsNotElementType().ToElements()
        typeIds = []
        # get element instances
        for ele in elements:
            typeId = ""
            try:
                typeId = ele.LookupParameter('Type').AsElementId()
                if not typeId in typeIds:
                    typeIds.append(typeId)
            except:
                pass
        typeTitle = []
        # get Family Types
        for type in typeIds:
            # print(type)
            try:
                name = openedDoc.GetElement(type).LookupParameter('Type Name').AsString()
            except:
                name = ""
            typeLine = [title, name]
            # GEt Type parameters
            values = []
            try:
                values = get_parameters_as_dic(openedDoc.GetElement(type))
                # print(values)
            except:
                values = {}
            valueList = []
            for k in values.keys():
                valueList.append(k + ":" + values[k])
            typeAll = typeLine + valueList
            typeTitle.append(typeAll)
        EAMQcUtils.ExcelWriter(excelFile, 'TYPES', 0, 0, typeTitle)
        t.Commit()

        # Close Excel and Revit File
        excelFile.close()
        openedDoc.Close(False)
        print('File Saved' + fileName)



else:
    forms.alert('No File is selected', title='', sub_msg=None, expanded=None, footer='', ok=True, cancel=False,
                yes=False,
                no=False, retry=False, warn_icon=True, options=None, exitscript=False)