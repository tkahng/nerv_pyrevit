import clr, sys, re, os, imp
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Structure
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol,ElementId
from System.Collections.Generic import List
from Autodesk.Revit.UI import RibbonPanel
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
from pyrevit import script, DB, revit
from pyrevit import forms
import pyrevit
import ConfigParser
from os.path import expanduser
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Show All recorded items in Navisworks'

outprint = script.get_output()
path = r'\\stvgroup.stvinc.com\v3\DGPA\Vol3\Projects\3019262\3019262_0001\90_CAD Models and Sheets\17017000\_PIM\Data\NavisData'
filePath = forms.pick_file(file_ext='txt', multi_file=False, init_dir=path, unc_paths=False)
# print(script.get_all_buttons())
openedFile = open(filePath)
# lets create that config file for next time...
home = expanduser("~")



cfgfile = open(home + "\\STVTools.ini",'w')
Config = ConfigParser.ConfigParser()
# add the settings to the structure of the file, and lets write it out...
Config.add_section('NavisFilePath')
Config.set('NavisFilePath', 'DataPath', filePath)
Config.write(cfgfile)
cfgfile.close()
print("Data File Set to: " + filePath)

ribbons = uidoc.Application.GetRibbonPanels("STVTools")
for i in ribbons:
    if i.Name == "Navis Data Import":
        buttons = i.GetItems()
        for b in buttons:
            if b.Name == 'Display':
                if len(filePath) > 0:
                    b.Enabled = True
                else:
                    b.Enabled = False

