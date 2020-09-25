
import sys, clr, re, bs4
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



# body
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, FamilySymbol,Transaction,\
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, ViewSchedule, View, ImportInstance, XYZ, \
    BuiltInParameter
from Autodesk.Revit.UI import RevitCommandId, PostableCommand, TaskDialog
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
import time
uiapp = UIApplication(doc.Application)
application = uiapp.Application
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script, coreutils
from pyrevit import forms

# logging module
import logging
import datetime
userName = application.Username
logFile = '\\\\Uspadgv1dcl01\\NY BIM GROUP\\Tools\\Repo\\pyRevit_custom_STV\\logs\\' + str(datetime.date.today()) + "_" + userName + '_applog.log'
logging.basicConfig(filename=logFile, filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')



def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)


from System import EventHandler, Uri
from pyrevit import framework
from pyrevit import script
from pyrevit import DB, UI
from Autodesk.Revit.DB import TextNoteType
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs, IdlingEventArgs
clr.AddReferenceByPartialName('System.Windows.Forms')
from System.Windows.Forms import SendKeys


elements = get_selected_elements(doc)
for instance in elements:
    workset = instance.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsValueString()
    id = instance.Id
    print(id.ToString() + ', ' + workset)
