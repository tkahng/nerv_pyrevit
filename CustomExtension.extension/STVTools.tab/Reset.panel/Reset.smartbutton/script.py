import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from System.Collections.Generic import List
from Autodesk.Revit.UI import RibbonPanel
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
from pyrevit import script, DB, revit, UI
from pyrevit import forms
import pyrevit
from pyrevit import framework
import ConfigParser
from os.path import expanduser
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')

outprint = script.get_output()

filePath = ''
# print(script.get_all_buttons())

# lets create that config file for next time...
home = expanduser("~")
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    '''
    __rvt__.DocumentOpened += \
        framework.EventHandler[
            UI.Events.RibbonItemEventArgs](SetbuttonStatus)
            '''
    cfgfile = open(home + "\\STVTools.ini",'w')
    Config = ConfigParser.ConfigParser()
    # add the settings to the structure of the file, and lets write it out...
    Config.add_section('NavisFilePath')
    Config.set('NavisFilePath','DataPath',' ')
    Config.write(cfgfile)
    cfgfile.close()
    ribbons = __rvt__.GetRibbonPanels("STVTools")
    for i in ribbons:
        if i.Name == "Navis Data Import":
            buttons = i.GetItems()
            for b in buttons:
                if b.Name == 'Display':
                    b.Enabled = False

