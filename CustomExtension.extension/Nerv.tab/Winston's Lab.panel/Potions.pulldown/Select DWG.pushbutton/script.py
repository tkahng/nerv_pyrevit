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
import time
from Autodesk.Revit.DB import Document,FilteredElementCollector, PerformanceAdviser, FamilySymbol,\
    Transaction,FailureHandlingOptions, CurveElement, ImportInstance
from Autodesk.Revit.UI import TaskDialog, RevitCommandId, PostableCommand
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import SendKeys
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
'''
destinationFolder = forms.pick_folder()
print(destinationFolder)
'''

__doc__ = 'Select DWG imports'

def CadImportsName(doc):
    collector = FilteredElementCollector(doc)
    linkInstances = collector.OfClass(ImportInstance)
    linkName = []
    for i in linkInstances:
        name = str(i.LookupParameter("Name").AsString())
        if not name in linkName and not i.IsLinked:
            linkName.append(name)
    return linkName

def CadImportsbyName(doc, names):
    collector = FilteredElementCollector(doc)
    linkInstances = collector.OfClass(ImportInstance)
    link = []
    for i in linkInstances:
        if str(i.LookupParameter("Name").AsString()) in names and not i.IsLinked:
            link.append(i)
    return link

dwgs = CadImportsName(doc)
picked = sel_action = forms.SelectFromList.show(dwgs, button_name='Select Item', multiselect=True)
links = CadImportsbyName(doc,picked)
revit.get_selection().set_to(links)
