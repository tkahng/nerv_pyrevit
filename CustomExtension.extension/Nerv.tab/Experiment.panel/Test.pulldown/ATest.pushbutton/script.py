
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
    Workset, FilteredWorksetCollector, WorksetKind, RevitLinkType, RevitLinkInstance, View3D, ViewType,ElementClassFilter,\
    ViewFamilyType, ViewFamily, BuiltInParameter, IndependentTag, Reference, TagMode, TagOrientation
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs
from pyrevit import revit, DB, forms
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit import framework
from pyrevit import script
from pyrevit import DB, UI
import datetime, os
from pyrevit import HOST_APP, framework
'''
t = Transaction(doc, 'Tag Selected Element')
t.Start()
selection = Selection.get_selected_elements(doc)
for a in selection:
    location = a.Location
    IndependentTag.Create(doc, doc.ActiveView.Id, Reference(a), True, TagMode.TM_ADDBY_MULTICATEGORY, TagOrientation.Horizontal, location.Point)
    print(location.Point)
t.Commit()
'''
print(str(datetime.date.today()))

class Logger:
    # File location for logging
    #fileLocation = ""
    # Constructor
    def __init__(self, address):
        self.fileLocation = address
    #Logger
    def Log(self, content, user):
        date = datetime.datetime
        if not os.path.exists(self.fileLocation):
            logFile = open(self.fileLocation, "w")
            logFile.write(str(datetime.date.today()) + "_" + user + "_" + "Log Start")
            logFile.close()

        try:
            writeFile = open(self.fileLocation, "a+")
            writeFile.write(content)
            writeFile.close()
        except:
            print("Failed")
logger = Logger("\\\\stvgroup.stvinc.com\\p\\NYNY\\Practices\\Hazem Kahla\\RevitLogs\\" + str(datetime.date.today()) + "_" + str(doc.Application.Username)+ ".txt" )

separator = ","
docTitle = doc.Title
message = str(datetime.datetime)

logger.Log(message, str(doc.Application.Username))
print(HOST_APP.app)

def event_handler_function(sender, args):
   print("View activating")
   event_uidoc = sender.ActiveUIDocument
   event_doc = sender.ActiveUIDocument.Document
# I'm using ViewActivating event here as example.
# The handler function will be executed every time a Revit view is activated:
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    try:
        __rvt__.Application.DocumentChanged += framework.EventHandler[DB.Events.DocumentChangedEventArgs](event_handler_function)
        return True
    except Exception:
        return False