import clr
import pprint
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")

doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Info about this panel,'\
          'and also who can you talk to if you need help.'

info = ['These tools are developed by Mengfan Lou using pyRevit which is Created by eirannejad or Ehsan Iran-Nejad.'
        'For internal use only.',
        'Panel Developed by: Martin Lou', 'Contact Info:', 'mengfan.lou@stvinc.com',
        '(p)(212)505-4978 (c)(646)556-5711', 'STV INC. 225 PARK AVENUE SOUTH, NEW YORK, NY 10003']

pp = pprint.PrettyPrinter(indent = 4)
pp.pprint(info)