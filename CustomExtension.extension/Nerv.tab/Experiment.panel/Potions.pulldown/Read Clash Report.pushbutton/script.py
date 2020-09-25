
import sys, clr, re, bs4
import ConfigParser
from os.path import expanduser
from bs4 import BeautifulSoup
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
    FailureHandlingOptions, CurveElement, BuiltInCategory, ElementId, ViewSchedule, View, ImportInstance, XYZ
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
from pyrevit import forms, coreutils

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

import bs4, soupsieve
from System import EventHandler, Uri
from pyrevit import framework
from pyrevit import script
from pyrevit import DB, UI
from Autodesk.Revit.DB import TextNoteType, Viewport
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs, IdlingEventArgs
clr.AddReferenceByPartialName('System.Windows.Forms')
from System.Windows.Forms import SendKeys
from pyrevit import script

__doc__ = 'Open Clash Report in a website with clickable element id'

output = script.get_output()

collectorFile = forms.pick_file(file_ext='html', multi_file=False, unc_paths=False)
ElementIDRegex = re.compile(r'Element ID:\D+?\d+')
IDRegex = re.compile(r'\d+')

clashFile = open(collectorFile)
clashSoup = bs4.BeautifulSoup(clashFile, "html.parser")
pnt = clashSoup.select('body')
# Locate clash data
clashData = pnt[0].getText()
# Find the first row of Element ID
elementID = ElementIDRegex.findall(clashData)
elementIDPool = []
for i in elementID:
    elementIDP = str(IDRegex.findall(i))
    elementIDPool.append(elementIDP)
currentID = elementIDPool[:: 2]
otherID = elementIDPool[1:: 2]
# Replacement Id

# Read in the file
with open(collectorFile, 'r') as file :
  filedata = file.read()

# get unique Items
unique = []
for x in elementIDPool:
    if x not in unique:
        unique.append(x)

# Write the file out again
for id in unique:
    idString = id[2:len(id)-2]
    a = ElementId(int(idString))
    link = coreutils.reverse_html(str(output.linkify(a)))
    #i.replace_with("<a " + str(link)[3: len(str(link)) - 3] + "/a>")
    replacement = "<a " + str(link)[3: len(str(link)) - 3] + "/a>"
    # Replace the target string
    filedata = filedata.replace(idString, replacement)

with open(collectorFile, 'w') as file:
    file.write(filedata)
'''
for id in currentID:
    idString = id[2:len(id)-2]
    a = ElementId(int(idString))
    link = coreutils.reverse_html(str(output.linkify(a)))
    source = clashSoup.find_all(text = re.compile(idString))
    for i in source:
        #i.replace_with("<a " + str(link)[3: len(str(link)) - 3] + "/a>")
         replacement = "<a " + str(link)[3: len(str(link)) - 3] + "/a>"
        # print("<a " + str(link)[3: len(str(link)) - 3] + "/a>")
    # print(str(link))

with open(collectorFile, "w") as file:
    file.write(str(clashSoup))
'''
output.open_page(collectorFile)


