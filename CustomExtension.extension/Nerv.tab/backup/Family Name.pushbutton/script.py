from pyrevit import revit, DB, forms
import clr,re
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
     Color, BuiltInParameter, TextNote, TextNoteType
from Autodesk.Revit.UI import UIApplication

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')

__doc__ = 'Modify family names according to PA standard.'

# Define the prefix we want to track and add
def UniqueName(proposedName, namesList):
    num = 1
    nameIteration = proposedName + ' ' + str(num)
    while num < 999:
        if not proposedName in namesList:
            return proposedName
            break
        elif not nameIteration in namesList:
            return nameIteration
            break
        else:
            num += 1
            nameIteration = proposedName + ' ' + str(num)
            continue

def FamilyNameChange(doc):
    namesLst = []
    family = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()
    for i in family:
        namesLst.append(i.Family.Name)
    exempt = ['Profiles', 'Section Marks', 'Curtain Panels', 'Section Marks', 'Generic Annotations', 'Callout Heads',
              'Level Heads', 'View Titles']
    familyRegex = re.compile(r'\S+.*\s?-\s?\S+.*\s?-\s?\S+.*?')
    for i in family:
        if not i.Family.FamilyCategory.Name in exempt and not 'Tag' in i.Family.FamilyCategory.Name:
            cate = i.Family.FamilyCategory.Name
            if cate != "Generic Models":
                familyName = i.Family.Name
                if familyName[0:2] == 'PA':
                    pass
                elif familyRegex.findall(familyName) == [] and familyName[0:2] != 'PA' and len(re.split('-', familyName)) <=1:
                    proposedName = UniqueName(cate + '-Generic-' + familyName, namesLst)
                    try:
                        i.Family.Name = proposedName
                    except:
                        pass
                    namesLst.append(proposedName)
                    print('Changed 1 ' + familyName + ' to ' + proposedName)

                elif familyRegex.findall(familyName) == [] and familyName[0:2] != 'PA' and len(re.split('-', familyName)) == 2 :
                    proposedName = UniqueName(cate + '-Generic-' + familyName.replace('-', '_'), namesLst)
                    try:
                        i.Family.Name = proposedName
                    except:
                        pass
                    namesLst.append(proposedName)
                    print('Changed 2 ' + familyName + ' to ' + proposedName)

                elif familyRegex.findall(familyName) != [] and familyName[0:len(cate)] != cate and familyName[0:len(cate)-1] != cate[0: len(cate) -1]\
                        and familyName[0:2] != 'PA':
                    proposedName = UniqueName(cate + '-' + 'Generic-' + familyName.replace('-', '_'), namesLst)
                    try:
                        i.Family.Name = proposedName
                    except:
                        pass
                    namesLst.append(proposedName)
                    print('Changed 3 ' + familyName + ' to ' + proposedName)
            else:
                print("GENERIC MODEL EXCEPTION, NOT CHANGED!")



# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'WARNING: will delete line styles ' \
          'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application

# Select Action Item
actionList = ['Auto complete family name']
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

# Transaction Start
t = Transaction(doc, 'Add PA prefix to Name')
t.Start()
if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False,
                yes=False,
                no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Auto complete family name' in sel_action:
        FamilyNameChange(doc)
    else:
        pass
t.Commit()