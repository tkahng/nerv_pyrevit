import clr
import os
import pprint
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")

doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Open the word document showing all instructions of the tools.'

#os.startfile(r'\\Uspadgv1dcl01\BIM - B&F\00 - BIM Resources\06_BIM Tools\04-pyRevit\Instruction.docx')

#os.startfile(r'https://stvinc.sharepoint.com/sites/BIMNY/Shared Documents/B&F_BIM Documents/General/Nerv.docx')

info = ['The Instruction document is under construction.']

pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(info)