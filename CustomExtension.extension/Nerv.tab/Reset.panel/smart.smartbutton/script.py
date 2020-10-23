#pylint: disable=C0103,E0401
from pyrevit import script
from pyrevit.coreutils.ribbon import ICON_MEDIUM
from Autodesk.Revit.DB import Document, \
        OpenOptions, WorksetConfiguration, WorksetConfigurationOption, DetachFromCentralOption, \
        ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions
import System
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from System import Guid
from os.path import expanduser
import ConfigParser
import clr,sys, datetime
import os.path
from os import path
from pyrevit import HOST_APP, framework
from pyrevit import script
from pyrevit import DB, UI
from pyrevit import framework
from System import EventHandler, Uri
from Autodesk.Revit.UI.Events import ViewActivatedEventArgs, ViewActivatingEventArgs
from Autodesk.Revit.DB.Events import DocumentChangedEventArgs
__title__ = 'Reset'
__context__ = 'zero'


def event_handler_function(sender, args):
   print("View activating")

# I'm using ViewActivating event here as example.
# The handler function will be executed every time a Revit view is activated:


config = script.get_config()

def OpenCloudFiles(modelGUID, projectGUID, app, audit):
    openOpt = OpenOptions()
    if audit == True:
        openOpt.Audit = True
    else:
        openOpt.Audit = False
    # openOpt.DetachFromCentralOption = DetachFromCentralOption.DetachAndPreserveWorksets
    wsopt = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
    # wsopt.Open(worksetList)
    openOpt.SetOpenWorksetsConfiguration(wsopt)
    modelPath = ModelPathUtils.ConvertCloudGUIDsToCloudPath(projectGUID, modelGUID)
    currentdoc = app.OpenDocumentFile(modelPath, openOpt)
    try:
        DialogBoxShowingEventArgs.OverrideResult(1)
    except:
        pass
    return currentdoc

def SaveCloudModel(document, filePath):
    worksharingOptions = WorksharingSaveAsOptions()
    worksharingOptions.SaveAsCentral = True
    saveOpt = SaveAsOptions()
    saveOpt.SetWorksharingOptions(worksharingOptions)
    saveOpt.OverwriteExistingFile = True
    saveOpt.Compact = True
    document.SaveAs(filePath + document.Title + ".rvt", saveOpt)
    document.Close()

def SaveCloudModelandChangeName(document, filePath, Name):
    worksharingOptions = WorksharingSaveAsOptions()
    worksharingOptions.SaveAsCentral = True
    saveOpt = SaveAsOptions()
    saveOpt.SetWorksharingOptions(worksharingOptions)
    saveOpt.OverwriteExistingFile = True
    saveOpt.Compact = True
    document.SaveAs(filePath + Name + ".rvt", saveOpt)
    document.Close()

class Logger:
    # File location for logging
    fileLocation = ""
    # Constructor
    def __init__(self, address):
        self.fileLocation = address
    #Logger
    def Log(self, content, user):
        date = datetime.datetime
        if not path.exists(self.fileLocation):
            logFile = open(self.fileLocation, "w")
            logFile.write(str(datetime.datetime) + "_" + user + "_" + "Log Start")
            logFile.close()

        try:
            writeFile = open(self.fileLocation, "a+")
            writeFile.write(content)
            writeFile.close()
        except:
            print("Failed")

def log_function(sender, args):
    event_uidoc = sender.ActiveUIDocument
    event_doc = sender.ActiveUIDocument.Document
    logger = Logger("\\\\stvgroup.stvinc.com\\p\\NYNY\\Practices\\Hazem Kahla\\RevitLogs\\"
                    + str(datetime.date.today()) + "_" +
                    str(sender.ActiveUIDocument.Document.Application.Username) + ".txt" )
    separator = ","
    docTitle = args.GetDocument().Title
    message = str(datetime.datetime) + \
              " ;_Title:" + docTitle + \
              " ;_Transactions:" + separator.join(args.GetTransactionNames()) + \
              " ;_Added:" + separator.join(args.GetAddedElementIds()) + \
              " ;_Deleted:" + separator.join(args.GetDeletedElementIds()) + \
              " ;_Modified:" + separator.join(args.GetModifiedElementIds())
    logger.Log(message, sender.ActiveUIDocument.Document.Application.Username)

def test_function(sender, args):
    print("test")

# do the even stuff here


# FIXME: need to figure out a way to fix the icon sizing of toggle buttons
def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    #try:
    #__rvt__.Application.DocumentChanged += (Logger.test_function)
    #__rvt__.ViewActivating += EventHandler[ViewActivatingEventArgs](event_handler_function)
    #__rvt__.Application.DocumentChanged += framework.EventHandler[DB.Events.DocumentChangedEventArgs](log_function)
    HOST_APP.app.DocumentChanged += framework.EventHandler[DB.Events.DocumentChangedEventArgs](log_function)
    #except:
        #print("Logging Disabled.")
    #message =

    filePath = "C:\\Users\\loum\\Desktop\\acad\\"
    modelGUID = Guid("e77aa560-8776-4a0e-8192-3044c5e240df")
    projectGUID = Guid("20ac335a-5ba8-4520-b948-296e529c3306")

    # lets create that config file for next time...
    home = expanduser("~")
    '''
    __rvt__.DocumentOpened += \
        framework.EventHandler[
            UI.Events.RibbonItemEventArgs](SetbuttonStatus)
            '''
    # cfgfile = open(home + "\\STVTools.ini",'w')
    Config = ConfigParser.ConfigParser()
    Config.read(home + "\\STVTools.ini")
    # add the settings to the structure of the file, and lets write it out...
    try:
        Config.add_section('NavisFilePath')
        Config.set('NavisFilePath', 'DataPath', ' ')

        # Add master new system folder setting
        Config.add_section('SysDir')
        Config.set('SysDir', 'MasterPackage',
                   r'\\Uspadgv1dcl01\NY BIM GROUP\Tools\Repo\pyRevit_custom_STV\CustomExtension.extension\packages\\')
        Config.set('SysDir', 'SecondaryPackage',
                   r'\\Uspadgv1dcl01\BIM - B&F\00 - BIM Resources\06_BIM Tools\04-pyRevit\STVTools\CustomExtension.extension\packages\\')
    except:
        pass
    cfgfile = open(home + "\\STVTools.ini", 'w')
    Config.write(cfgfile)
    sys.path.append(r'\\Uspadgv1dcl01\NY BIM GROUP\Tools\Repo\pyRevit_custom_STV\CustomExtension.extension\packages\\')

    modelsDic = dict(Config.items('Cloud'))

    pyCfgFile = open(home + "\\STVTools.ini", 'w')
    Config.write(cfgfile)
    if Config.get('General', 'clouddownload') == "1":
        n = 1
        for i in modelsDic.values():
            list = i.split(";")
            modelGUID = Guid(list[0])
            projectGUID = Guid(list[1])
            modelFilePath = list[2]
            appVersion = str(list[3])
            name = str(list[4])
            if str(__rvt__.Application.VersionName) == appVersion:
                openedDoc = OpenCloudFiles(modelGUID, projectGUID, __rvt__.Application, audit=False)
                SaveCloudModelandChangeName(openedDoc, modelFilePath, name)
                print("Cloud Download Complete")
            else:
                print("Model {} was not downloaded due to version mismatch".format(str(n)))
            n += 1

    cfgfile.close()
    '''
    ribbons = __rvt__.GetRibbonPanels("STVTools")
    for i in ribbons:
        if i.Name == "Navis Data Import":
            buttons = i.GetItems()
            for b in buttons:
                if b.Name == 'Display':
                    b.Enabled = False
    '''
    return True

if __name__ == '__main__':
    print('Please do not click this button again.')