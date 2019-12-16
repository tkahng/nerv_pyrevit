
import clr
import time
import logging
import datetime

from pyrevit import framework
from pyrevit import script
from pyrevit import DB, UI, revit
from Autodesk.Revit.DB import ElementId
from Autodesk.Revit.UI import RevitCommandId, PostableCommand, TaskDialog, UIApplication
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

'''
def sendKey(sender, args):

    if script.get_envvar(SYNC_VIEW_ENV_VAR):
        event_uidoc = sender.ActiveUIDocument
        event_doc = sender.ActiveUIDocument.Document
        active_ui_views = event_uidoc.GetOpenUIViews()
        current_ui_view = None
        # TaskDialog.Show("Test", "Test")
        # Wait for 5 seconds
        uidoc = __revit__.ActiveUIDocument
        doc = __revit__.ActiveUIDocument.Document
        uiapp = UIApplication(doc.Application)

        elements = get_selected_elements(doc)
        for ele in elements:
            revit.get_selection().set_to(ele)
            time.sleep(0.5000)
            SendKeys.SendWait("+{K}")
            time.sleep(0.2000)
            #SendKeys.SendWait("{K}")
'''

def sendKey(sender, args):
    global elements
    global ROTATION_KEY
    # logging.debug("Key Mod Start")
    if script.get_envvar(SYNC_EXPLODE_ENV_VAR) and ROTATION_KEY == "STATEONE":
        # logging.debug("Selection Activate successful")
        # SYNC_EXPLODE_ENV_VAR = "EXPLODEINACTIVE"
        # logging.debug("Selection Program Status inactive")
        f = open("U:\\B52\\ids.txt", "r")
        ele = f.readline().split(",")
        e = ele[0]
        event_doc = sender.ActiveUIDocument.Document
        f.close()
        line = ""
        # elements = get_selected_elements(event_doc)
        logging.debug("Selection setting to first Element of list")
        # TaskDialog.Show("Count 4", str(len(elements)))
        revit.get_selection().set_to(event_doc.GetElement(ElementId(int(e))))
        for k in ele[1:]:
            line += k + ","
        updateLine = line[0: len(line) - 1]
        w = open("U:\\B52\\ids.txt", "w")
        w.write(updateLine)
        w.close()
        ROTATION_KEY = "STATETWO"
    elif script.get_envvar(SYNC_EXPLODE_ENV_VAR) and ROTATION_KEY == "STATETWO":
        logging.debug("Key Press Start!")
        time.sleep(1)
        # SendKeys.SendWait("+{K}")

        # TaskDialog.Show("Count Total", str(len(elements)))
        '''
        while True:
            logging.debug("Key loop start")
            if len(get_selected_elements(event_doc)) == 1:
                logging.debug("Key selection 1 confirmed")
                time.sleep(1)
                logging.debug("Key sleep for 1 seconds ended")
                #TaskDialog.Show("Count Current", str(len(get_selected_elements(doc))))
                #time.sleep(1)
                logging.debug("Key Press Start!")
                SendKeys.SendWait("+{K}")
                time.sleep(1)
                # TaskDialog.Show("Count Total", str(len(elements)))
                logging.debug("Key Press End!")
                # MessageBox.Show("wedwad")
                break
            else:
                logging.debug("Key loop return")
                return
            '''
        # TaskDialog.Show("Count 1", str(len(elements)))
        logging.debug("Key Setting Selection to global")
        # revit.get_selection().set_to(elements[1:])
        # elements = elements[1:]
        # revit.get_selection().set_to(elements[1:])
        time.sleep(1)
        logging.debug("Key Set Selection successful")
        ROTATION_KEY = "STATEONE"



'''
def sendSelection(sender, args):
    global elements
    global SYNC_EXPLODE_ENV_VAR
    # logging.debug("Selection Mod Start")
    if script.get_envvar(SYNC_EXPLODE_ENV_VAR): # and SYNC_EXPLODE_ENV_VAR == "EXPLODEACTIVE":
        # logging.debug("Selection Activate successful")
        # SYNC_EXPLODE_ENV_VAR = "EXPLODEINACTIVE"
        # logging.debug("Selection Program Status inactive")
        event_doc = sender.ActiveUIDocument.Document
        logging.debug("Selection getting selected elements")
        elements = get_selected_elements(event_doc)
        logging.debug("Selection setting to first Element of list")
        # TaskDialog.Show("Count 4", str(len(elements)))
        revit.get_selection().set_to(event_doc.GetElement(str(elements[0])))
        revit.get_selection().set_to(event_doc.GetElement(ElementId(int(elements[0]))))
        logging.debug("Selection set to first element success!")
        # TaskDialog.Show("Count 5", str(len(elements))
        # SYNC_EXPLODE_ENV_VAR = "EXPLODEACTIVE"
        # logging.debug("Selection Program Status Active")
'''
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
        # logging.debug("Parent Selection mod start")
        # __rvt__.Idling += framework.EventHandler[IdlingEventArgs.SetRaiseWithoutDelay()](sendSelection)
        # logging.debug("Parent Selection mod end")
        # logging.debug("Parent Key mod start")
        __rvt__.Idling += framework.EventHandler[IdlingEventArgs](sendKey)
        # logging.debug("Parent Key mod end")
        # __rvt__.Idling += framework.EventHandler[IdlingEventArgs](PopWindow)\
        # logging module
        return True
    except Exception:
            logging.debug("Program Fail")
            return False


if __name__ == '__main__':
    togglestate()





