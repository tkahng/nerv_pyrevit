
import clr
import time
import logging
import datetime

from pyrevit import framework
from pyrevit import script
from pyrevit import DB, UI, revit
from Autodesk.Revit.DB import ElementId
from Autodesk.Revit.UI import RevitCommandId, PostableCommand, TaskDialog, UIApplication, UIDocument
from Autodesk.Revit.UI.Selection import Selection
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs, IdlingEventArgs
from Autodesk.Revit.DB.Events import DocumentChangedEventArgs
clr.AddReferenceByPartialName('System.Windows.Forms')
from System.Windows.Forms import SendKeys, MessageBox
__doc__ = 'Keep views synchronized. This means that as you pan and zoom and '\
          'switch between Plan and RCP views, this tool will keep the views '\
          'in the same zoomed area so you can keep working in the same '\
          'area without the need to zoom and pan again.\n'\
          'This tool works best when the views are maximized.'

logFile = '\\\\Uspadgv1dcl01\\NY BIM GROUP\\Tools\\Repo\\pyRevit_custom_STV\\logs\\' + str(
    datetime.date.today()) + "_"  + '_General_Applog.log'
logging.basicConfig(level = logging.DEBUG, filename=logFile, filemode='w', format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

elements = []

SYNC_EXPLODE_ENV_VAR = 'EXPLODEACTIVE'
ROTATION_KEY = 'STATEONE'

def sendKey(sender, args):
    global elements
    global ROTATION_KEY

    if script.get_envvar(SYNC_EXPLODE_ENV_VAR) and ROTATION_KEY == "STATEONE":
        f = open("U:\\B52\\ids.txt", "r")
        ele = f.readline().split(",")
        e = ele[0]
        event_doc = sender.ActiveUIDocument.Document
        f.close()
        line = ""
        logging.debug("Selection setting to first Element of list")
        explodeElement = event_doc.GetElement(ElementId(int(e)))
        '''
        # Activate View
        viewId = explodeElement.OwnerViewId
        ownerView = event_doc.GetElement(viewId)
        sender.ActiveView = ownerView
        time.sleep(0.5)
        '''
        revit.get_selection().set_to(explodeElement)
        for k in ele[1:]:
            line += k + ","
        updateLine = line[0: len(line) - 1]
        w = open("U:\\B52\\ids.txt", "w")
        w.write(updateLine)
        w.close()
        ROTATION_KEY = "STATETWO"

    elif script.get_envvar(SYNC_EXPLODE_ENV_VAR) and ROTATION_KEY == "STATETWO":
        pass
        
        logging.debug("Key Press Start!")
        time.sleep(0.5)
        # TaskDialog.Show("Count 1", str(len(elements)))
        logging.debug("Key Setting Selection to global")
        # revit.get_selection().set_to(elements[1:])
        # elements = elements[1:]
        # revit.get_selection().set_to(elements[1:])
        logging.debug("Key Set Selection successful")
        
        ROTATION_KEY = "STATEONE"

def PopWindow(sender, args):
    global elements
    if script.get_envvar(SYNC_EXPLODE_ENV_VAR):
        TaskDialog.Show("Test", "Idle")


def togglestate():
    new_state = not script.get_envvar(SYNC_EXPLODE_ENV_VAR)
    script.set_envvar(SYNC_EXPLODE_ENV_VAR, new_state)
    script.toggle_icon(new_state)


# noinspection PyUnusedLocal
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    try:
        __rvt__.Idling += framework.EventHandler[IdlingEventArgs](sendKey)
        return True
    except Exception:
            logging.debug("Program Fail")
            return False


if __name__ == '__main__':
    togglestate()





