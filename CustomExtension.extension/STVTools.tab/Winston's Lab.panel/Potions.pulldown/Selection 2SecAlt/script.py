'''
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

def sendKey(sender, args):
    global elements
    if script.get_envvar(SYNC_EXPLODE_ENV_VAR):
        event_doc = sender.ActiveUIDocument.Document
        elements = get_selected_elements(event_doc)

        while True:
            f = open("C:\\Users\\loum\\Desktop\\New folder\\ids.txt", "r")
            ele = f.readline()
            f.close()
            if ele == "1":
                logging.debug("Selection getting selected elements")

                revit.get_selection().set_to(elements[1:])
                logging.debug("Selection updated")
                w = open("C:\\Users\\loum\\Desktop\\New folder\\ids.txt", "w")
                w.write("0")
                w.close()
                logging.debug("Write Completed")
                time.sleep(1)
                break
            else:
                revit.get_selection().set_to(elements[0])
                logging.debug("Selection Completed")
                time.sleep(1)
                return




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
'''
import os
import os.path as op
import pickle as pl
import clr
import time

from pyrevit import framework
from pyrevit import script
from pyrevit import DB, UI, revit
from Autodesk.Revit.UI import RevitCommandId, PostableCommand, TaskDialog, UIApplication
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs, IdlingEventArgs
from Autodesk.Revit.DB.Events import DocumentChangedEventArgs
clr.AddReferenceByPartialName('System.Windows.Forms')
from System.Windows.Forms import SendKeys
__doc__ = 'Keep views synchronized. This means that as you pan and zoom and '\
          'switch between Plan and RCP views, this tool will keep the views '\
          'in the same zoomed area so you can keep working in the same '\
          'area without the need to zoom and pan again.\n'\
          'This tool works best when the views are maximized.'


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
SYNC_VIEW_ENV_VAR = 'SYNCVIEWACTIVE'
# todo: sync views - 3D

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
    if script.get_envvar(SYNC_VIEW_ENV_VAR):
        event_doc = sender.ActiveUIDocument.Document
        uiapp = UIApplication(event_doc.Application)
        while True:
            if len(get_selected_elements(event_doc)) == 1:
                time.sleep(1)
                # TaskDialog.Show("Count Total", str(len(elements)))
                #TaskDialog.Show("Count Current", str(len(get_selected_elements(doc))))
                #time.sleep(1)
                # SendKeys.SendWait("+{K}")

                break
            else:
                return
        # TaskDialog.Show("Count 1", str(len(elements)))

        revit.get_selection().set_to(elements[1:])
        # TaskDialog.Show("Count 2", str(len(elements)))


def sendSelection(sender, args):
    global elements
    if script.get_envvar(SYNC_VIEW_ENV_VAR):
        event_doc = sender.ActiveUIDocument.Document
        # TaskDialog.Show("Count 3", str(len(elements)))

        elements = get_selected_elements(event_doc)

        # TaskDialog.Show("Count 4", str(len(elements)))
        revit.get_selection().set_to(elements[0])
        # TaskDialog.Show("Count 5", str(len(elements)))

def togglestate():
    new_state = not script.get_envvar(SYNC_VIEW_ENV_VAR)
    script.set_envvar(SYNC_VIEW_ENV_VAR, new_state)
    script.toggle_icon(new_state)


# noinspection PyUnusedLocal
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    try:
        __rvt__.Idling += framework.EventHandler[IdlingEventArgs](sendSelection)

        __rvt__.Idling += framework.EventHandler[IdlingEventArgs](sendKey)

        return True
    except Exception:
            return False


if __name__ == '__main__':
    togglestate()







