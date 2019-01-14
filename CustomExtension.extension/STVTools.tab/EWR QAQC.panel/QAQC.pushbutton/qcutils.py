from pyrevit.framework import List
from pyrevit import revit, DB, forms

import clr
import os
import xlsxwriter
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, \
	OpenOptions,WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption,\
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions,GraphicsStyleType, BuiltInCategory

from System.Collections.Generic import List
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.ApplicationServices import Application
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')


def ExcelWriter(filePath, SheetName, startRow, startCol,list,choplength):

    return False

def LineCheck(doc):
    lines = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
    lineStyle = []
    for i in lines:
        lineStyle.append(i.Name)
        lineStyle.append(i.LineColor.Red)
        lineStyle.append(i.LineColor.Green)
        lineStyle.append(i.LineColor.Blue)
        lineStyle.append(i.GetLineWeight(GraphicsStyleType.Projection))
    return lineStyle
