from pyrevit.framework import List
from pyrevit import revit, DB
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Print Project Base Point, Survey Point, Shared Point parameters.'

basePt = DB.FilteredElementCollector(doc)\
              .OfCategory(BuiltInCategory.OST_Site)\
              .ToElements()
outProjBasePt = []
outProjSurvPt = []
for e in basePt:
    a = e.Category.Name
    if a == "Project Base Point":
        pbpEW = e.LookupParameter("E/W")
        pbpNS = e.LookupParameter("N/S")
        pbpElev = e.LookupParameter("Elev")
        pbpAngle = e.LookupParameter("Angle to True North")
        outProjBasePt.append(round(pbpEW.AsDouble()*ft2mm,6))
        outProjBasePt.append(round(pbpNS.AsDouble()*ft2mm,6))
        outProjBasePt.append(round(pbpElev.AsDouble()*ft2mm,6))
        outProjBasePt.append(round(pbpAngle.AsDouble()*180/math.pi,6))
    elif a == "Survey Point":
        pspEW = e.LookupParameter("E/W")
        pspNS = e.LookupParameter("N/S")
        pspElev = e.LookupParameter("Elev")
        outProjSurvPt.append(round(pspEW.AsDouble()*ft2mm,6))
        outProjSurvPt.append(round(pspNS.AsDouble()*ft2mm,6))
        outProjSurvPt.append(round(pspElev.AsDouble()*ft2mm,6))
print(outProjBasePt)
print(outProjSurvPt)

siteEle = DB.FilteredElementCollector(doc)\
              .OfClass(BasePoint)\
              .ToElements()
SharedPoint = []
for e in siteEle:
    if e.Location != None:
        pp = e.GetParameters('Family')
        for p in pp:
            if p.AsValueString() == 'Shared Point':
                siteLoc = e.Location
                sitePin = e.Pnned
                siteWork = e.WorksetId
                siteDis = e.GetParameters('Discipline')
                SharedPoint.append(siteDis,sitePin,siteWork,siteLoc)
print(SharedPoint)