
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

import System, Selection
import System.Threading, System.Threading.Tasks
from Autodesk.Revit.DB import Document, FilteredElementCollector, GraphicsStyle, Transaction, BuiltInCategory, RevitLinkInstance, UV, XYZ,SpatialElementBoundaryOptions, CurveArray
from Autodesk.Revit.DB import Level, BuiltInParameter
from Autodesk.Revit.UI import TaskDialog
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
import System.Windows.Forms
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
from pyrevit.framework import List
from pyrevit import revit, DB
import os
from collections import defaultdict
from pyrevit import script
from pyrevit import forms
from Autodesk.Revit.UI import TaskDialog, UIApplication
from math import *

__doc__ = 'Import rooms to space from link model'


links = FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements()
linkdocs = []
for i in links:
	linkdocs.append(i.GetLinkDocument())
linkrooms = []
for linkdoc in linkdocs:
	try:
		linkrooms.append(FilteredElementCollector(linkdoc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements())
	except:
		pass
levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
'''
linkrooms = []
linkrooms.append(FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements())
levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
'''
t = Transaction(doc, 'Create Spaces')
t.Start()
for g_rooms in linkrooms:
	for room in g_rooms:
		if room.Area > 0:
			list = []
			message = []
			cArray = CurveArray()
			pt = room.Location.Point
			uv = UV(pt.X, pt.Y)
			elev = round(room.Level.Elevation)
			level2 = None
			for level in levels:
				elev2 = round(level.Elevation)
				if elev == elev2:
					level2 = level


			if level2 is not None:
				if round(level2.Elevation) == round(doc.ActiveView.GenLevel.Elevation):
					name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
					number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
					height = room.get_Parameter(BuiltInParameter.ROOM_UPPER_OFFSET).AsDouble()
					sOptions = SpatialElementBoundaryOptions()
					sOptions.StoreFreeBoundaryFaces = True
					line = room.GetBoundarySegments(sOptions)
					for llist in line:
						for l in llist:
							ll = l.GetCurve()
							cArray.Append(ll)
				try:
					# doc.Create.NewSpaceBoundaryLines(doc.ActiveView.SketchPlane, cArray, doc.ActiveView)
					space = doc.Create.NewSpace(level2, uv)
					space.get_Parameter(BuiltInParameter.ROOM_NAME).Set(name)
					space.get_Parameter(BuiltInParameter.ROOM_NUMBER).Set(number)
					space.get_Parameter(BuiltInParameter.ROOM_UPPER_OFFSET).Set(height)

				except:
					pass
				# list.append(space)
t.Commit()

