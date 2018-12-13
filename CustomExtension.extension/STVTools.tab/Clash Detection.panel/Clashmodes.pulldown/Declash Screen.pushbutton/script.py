# -*- coding: UTF-8 -*-
"""print all clashes.

Lists all linked and imported DWG instances with worksets and creator.

Copyright (c) 2018 Martin Lou

--------------------------------------------------------

"""
import pyrevit
import clr
from collections import defaultdict
from pyrevit import revit, DB
from pyrevit import script
from pyrevit import forms
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Structure, DeleteElements
from Autodesk.Revit.DB import BuiltInCategory, ElementId, XYZ, Point, Transform, Transaction,FamilySymbol
from System.Collections.Generic import List
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


__title__ = 'Declash screen'
__author__ = 'Martin Lou'
__contact__ = 'mengfan.lou@stvinc.com'


__doc__ = 'Print Existing Clash  '\
          'This is helpful check project info'


# Clash point Calculation
FSymbol = DB.FilteredElementCollector(doc) \
    .OfCategoty(BuiltInCategory.OST_Site) \
    .ToElements()

clashPoints = []
for i in FSymbol:
    if i.Family.Name == 'Site-Generic-Clashpoint':
        clashPoints.append(i)

# Print Existing ClashPoints in the model
outprint = script.get_output()
output = pyrevit.output.get_output()
tab = ' '
secondCount = 0
for el in clashPoints:
    selSet.append(el.Id)
    idLen = len(Pointdata.clashName[secondCount])
    elId = Pointdata.clashName[secondCount][2: idLen - 2]
    idElement = ElementId(int(elId))
    print ('Clash No. ' + str(secondCount + 1) + tab + 'Clash Point: ' + format(outprint.linkify(el.Id)) + tab +
           'Clash Item: ' + format(outprint.linkify(idElement)))
    secondCount += 1



if not clashPoint:
    print('Please Load the Clash Point Family')
    print(clashPoint.Family.Name)
    print(clashPoint)
    count = 0
    elements = []
    for el in Pointdata.pointX:
        x = float(Pointdata.pointX[count]) + ew
        y = float(Pointdata.pointY[count]) + ns
        z = float(Pointdata.pointZ[count]) + elevation
        clashName = str('No. ' + str(count + 1) + ' ID: ' + Pointdata.clashName[count])
        clashwithID = str(Pointdata.otherFile[count] + ' ID: ' + Pointdata.clashwithID[count])
        pnt = XYZ(x,y,z)
        bPnt = Transform.CreateRotation(XYZ.BasisZ, angle).OfPoint(pnt)
        print(bPnt)

        # Clash point creation
        boxes = doc.Create.NewFamilyInstance(bPnt, clashPoint, Structure.StructuralType.NonStructural)
        elements.append(boxes)

        boxes.LookupParameter('Clash Name').Set(clashName)
        boxes.LookupParameter('Clash with ID').Set(clashwithID)
        count += 1


    selSet = []

    for el in elements:
        selSet.append(el.Id)


    revit.get_selection().set_to(selSet)


output = script.get_output()
def listclashes(current_view_only=False):
    dwgs = DB.FilteredElementCollector(revit.doc)\
             .OfClass(DB.ImportInstance)\
             .WhereElementIsNotElementType()\
             .ToElements()

    dwgInst = defaultdict(list)
    workset_table = revit.doc.GetWorksetTable()

    output.print_md("## LINKED AND IMPORTED DWG FILES:")
    output.print_md('By: [{}]({})'.format(__author__, __contact__))

    for dwg in dwgs:
        if dwg.IsLinked:
            dwgInst["LINKED DWGs:"].append(dwg)
        else:
            dwgInst["IMPORTED DWGs:"].append(dwg)

    for link_mode in dwgInst:
        output.print_md("####{}".format(link_mode))
        for dwg in dwgInst[link_mode]:
            dwg_id = dwg.Id
            dwg_name = dwg.LookupParameter("Name").AsString()
            dwg_workset = workset_table.GetWorkset(dwg.WorksetId).Name
            dwg_instance_creator = \
                DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc,
                                                              dwg.Id).Creator

            if current_view_only \
                    and revit.activeview.Id != dwg.OwnerViewId:
                continue

            print('\n\n')
            output.print_md("**DWG name:** {}\n\n"
                            "- DWG created by:{}\n\n"
                            "- DWG id: {}\n\n"
                            "- DWG workset: {}\n\n"
                            .format(dwg_name,
                                    dwg_instance_creator,
                                    output.linkify(dwg_id),
                                    dwg_workset))


selected_option = \
    forms.CommandSwitchWindow.show(
        ['In Current View',
         'In Model'],
        message='Select search option:'
        )

if selected_option:
    listdwgs(current_view_only=selected_option == 'In Current View')
