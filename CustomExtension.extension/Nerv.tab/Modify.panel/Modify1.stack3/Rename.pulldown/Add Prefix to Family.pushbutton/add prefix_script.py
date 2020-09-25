from pyrevit import revit, DB, forms
import clr, re
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, ImportInstance, BuiltInCategory, \
    ModelPathUtils, SaveAsOptions, WorksharingSaveAsOptions, Level, FilledRegionType, FamilySymbol, GraphicsStyleType, \
    CurveElement, Color, DimensionType, BuiltInParameter, Dimension
from Autodesk.Revit.UI import UIApplication
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')

__doc__ = 'Add custom prefix to families.'

# Collect Save location and Rvt Files
prefix  = 'PA - '

def SetDimensionStyle(doc, source, destination):
    elements = FilteredElementCollector(doc).OfClass(Dimension).ToElements()
    for i in elements:
        if i.LookupParameter('Type').AsValueString() == source:
            i.LookupParameter('Type').Set(destination.Id)

def SplitString(name):
    pieces = re.split(name)
    if '.dwg' in name:
        
        if len(pieces) >= 2:
            out = pieces[len(pieces)]


def AddPrefixtoAnnotation(doc):
        annotation = FilteredElementCollector(doc).OfClass(FamilySymbol)
        family = []
        familyName = []
        family_dict = {}
        for i in annotation:
            cate = i.Category.Name
            if cate == 'Generic Annotations' or 'Symbol' in cate or 'Tag' in cate or 'Annotation' in cate \
                    or 'Title' in cate or 'Mark' in cate or 'Head' in cate:
                if str(i.Family.Name)[0:len(prefix)] != prefix and not i.Family in family:
                    familyName.append(i.Family.Name)
                    family.append(i.Family)
                    for i in range(len(family)):
                        family_dict[familyName[i]] = family[i]
        sel_family = forms.SelectFromList.show(familyName, button_name='Select Item you want to add prefix to',
                                               multiselect=True)
        if not sel_family is None:
            for f in sel_family:
                changed_name = []
                name = family_dict[f].Name
                if name[0:len(prefix)] != prefix:
                    if not prefix + name in changed_name:
                        try:
                            print('Changing {0} to {1}'.format(family_dict[f].Name, prefix + name))
                            family_dict[f].Name = prefix + name
                            changed_name.append(family_dict[f].Name)
                        except:
                            print('Changing {0} to {1} -1'.format(family_dict[f].Name, prefix + name))
                            family_dict[f].Name = prefix + name + ' - 1'
                            changed_name.append(family_dict[f].Name)


# TODO Fix this Function
def AddPrefixtoDimension(doc):
    dimension = FilteredElementCollector(doc).OfClass(DimensionType).ToElements()
    for i in dimension:
        name = i.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        try:
            if i.Id.IntegerValue > 0 and name[0:len(prefix)] != prefix and str(name) != '':
                proposedName = prefix + name
                print(proposedName, i.Id.IntegerValue)
                destination = i.Duplicate(prefix + name)
                SetDimensionStyle(doc, name, destination)
                doc.Delete(i.Id)
                print('Renamed ' + name + ' to ' + proposedName)
        except:
            print(name + 'fail')


# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

#__doc__ = 'Open projects and resave in a specific location'\
            #'Please do not use lightly'
uiapp = UIApplication(doc.Application)
application = uiapp.Application


# Select Action Item
actionList = ['Add PA - to Annotation Symbol',
              'Add PA - to Dimension Symbol']
sel_action = forms.SelectFromList.show(actionList, button_name='Select Item', multiselect=True)

# Transaction Start
t = Transaction(doc, 'Add PA prefix to Name')
t.Start()

if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Add PA - to Annotation Symbol' in sel_action:
        AddPrefixtoAnnotation(doc)
    if 'Add PA - to Dimension Symbol' in sel_action:
        AddPrefixtoDimension(doc)
    else:
        pass
t.Commit()