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


def get_parameters_as_list(element, names):
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
            elif 'Double' in str(param.StorageType):
                _param[name] = str(param.AsDouble())
            elif 'ElementId' in str(param.StorageType):
                _param[name] = str(param.AsElementId().IntegerValue)
            else:
                _param[name] = "No Value"
    #print(_param)
    values = []
    for name in names:
        try:
            values.append(_param[name])
        except:
            values.append("n/a")
    return values

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
process = ["View Specific", "All Elements"]
pickedProcess = forms.SelectFromList.show(process, button_name='Select Item', multiselect=False)

if len(collectorFiles) > 0:
    for aDoc in collectorFiles:
        # Header of Excel file
        elementTitle = [['Model Name', 'Category', 'ElementID', 'TypeID', 'Mark']]
        typeTitle = [
            ['Model Name', 'TypeID', 'Type Name', 'Family Name', 'Assembly Code', 'Assembly Description', 'Model',
             'Manufacturer', 'Description']]

        # List of Parameters, Please expand
        elementParaList = ['Mark']
        typeParaList = ['Type Name', 'Family Name', 'Assembly Code', 'Assembly Description', 'Model', 'Manufacturer',
                        'Description']

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
        blank = []
        elements = ()
        #typesIds = FilteredElementCollector(openedDoc).WhereElementIsElementType().ToElementIds()
        typeIds = []
        # Create View
        if pickedProcess == "View Specific":
            threeDViews = []
            viewFamilyTypes = FilteredElementCollector(openedDoc).OfClass(ViewFamilyType).ToElements()
            for viewFa in viewFamilyTypes:
                if viewFa.ViewFamily == ViewFamily.ThreeDimensional:
                    threeDViews.append(viewFa.Id)
            # viewTypeId =  ViewType.ThreeD.Id
            view = View3D.CreateIsometric(openedDoc, threeDViews[0])
            # view.Name = "EAM View"
            elements = FilteredElementCollector(openedDoc, view.Id).WhereElementIsNotElementType().ToElements()
        # If all elements are selected
        elif pickedProcess == "All Elements":
            elements = FilteredElementCollector(openedDoc).WhereElementIsNotElementType().ToElements()

        # get element instances
        for ele in elements:
            try:
                cate = ele.Category.Name
            except:
                cate = ""
            id = ele.Id.ToString()
            typeId = ""
            try:
                typeId = ele.GetTypeId()
                if not typeId in typeIds:
                    typeIds.append(typeId)
            except:
                pass
            line = [title, cate, id, str(typeId.IntegerValue)]
            # Get Instance parameters
            for para in elementParaList:
                try:
                    value = ele.LookupParameter(para).AsString()
                except:
                    value = ""
                line.append(value)
            elementTitle.append(line)
        EAMQcUtils.ExcelWriter(excelFile, 'ELEMENTS', 0, 0, elementTitle)

        # get Family Types
        for type in typeIds:
            # print(type)
            typeLine = [title, str(type.IntegerValue)]
            # GEt Type parameters
            values = []
            try:
                values = get_parameters_as_list(openedDoc.GetElement(type), typeParaList)
                # print(values)
            except:
                values = []
            typeAll = typeLine + values
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