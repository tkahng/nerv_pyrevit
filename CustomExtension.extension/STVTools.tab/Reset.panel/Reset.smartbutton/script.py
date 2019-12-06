import clr,sys
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from System.Collections.Generic import List
from Autodesk.Revit.UI import RibbonPanel
from pyrevit import script, DB, revit, UI
from pyrevit import forms
import pyrevit
from pyrevit import framework
import ConfigParser
from os.path import expanduser
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs, IdlingEventArgs
from Autodesk.Revit.UI import RevitCommandId, PostableCommand, TaskDialog


# I'm using ViewActivating event here as example.
# The handler function will be executed every time a Revit view is activated:



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

    # Add master new system folder setting
    Config.add_section('SysDir')
    Config.set('SysDir', 'MasterPackage', r'\\Uspadgv1dcl01\NY BIM GROUP\Tools\Repo\pyRevit_custom_STV\CustomExtension.extension\packages\\')
    Config.set('SysDir', 'SecondaryPackage', r'\\Uspadgv1dcl01\BIM - B&F\00 - BIM Resources\06_BIM Tools\04-pyRevit\STVTools\CustomExtension.extension\packages\\')
    Config.write(cfgfile)
    sys.path.append(r'\\Uspadgv1dcl01\NY BIM GROUP\Tools\Repo\pyRevit_custom_STV\CustomExtension.extension\packages\\')
    cfgfile.close()
    ribbons = __rvt__.GetRibbonPanels("STVTools")
    for i in ribbons:
        if i.Name == "Navis Data Import":
            buttons = i.GetItems()
            for b in buttons:
                if b.Name == 'Display':
                    b.Enabled = False



