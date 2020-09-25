from pyrevit import revit, DB, forms
import clr, re
clr.AddReference('RevitAPI')
clr.AddReference("System")
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, BuiltInCategory, Views
from Autodesk.Revit.UI import UIApplication
clr. AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('PresentationFramework')
clr.AddReferenceByPartialName('System.Windows.Forms')
clr.AddReference('RevitAPIUI')

__doc__ = 'Add custom prefix to view names according to different view types.'

# ask for prefix input
prefix  = forms.ask_for_string(default='', prompt='Please input custom prefix', title='Custom Prefix')

# get all existing views names in order to avoid same view name
views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).ToElements()
viewNames = []
for view in views:
    vName = view.Name
    viewNames.append(vName)

def AddPrefixtoviews(doc, prefix, viewType):
    #views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).ToElements()
    for view in views:
    selectedViewName = []
    #family_dict = {}
    vType = view.ViewType.ToString()
        if vType == viewType:
            if str(view.Name)[0:len(prefix)] != prefix and not view.Name in viewNames:
                selectedViewName.append(view.Name)
    sel_view = forms.SelectFromList.show(selectedViewName, button_name='Select View(s) you want to add prefix to', multiselect=True)
 '''            
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
'''

# Main
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

uiapp = UIApplication(doc.Application)
application = uiapp.Application


# Select Action Item
actionList = ['Area Plan',
              'Ceiling Plan',
              'Detail View',
              'Drafting View',
              'Elevation',
              'Engineering Plan',
              'Floor Plan',
              'Legend',
              'Rendering',
              'Section',
              '3D View',
              'Walk through']
sel_action = forms.SelectFromList.show(actionList, button_name='Select View Type', multiselect=True)

# Transaction Start
t = Transaction(doc, 'Add Prefix To View')
t.Start()

if sel_action == None:
    forms.alert('No Action selected', title='Error', sub_msg=None, expanded=None, footer='', ok=True, cancel=False, yes=False,
                        no=False, retry=False, warn_icon=True, options=None, exitscript=False)
else:
    if 'Area Plan' in sel_action:
        AddPrefixtoviews(doc, AreaPlan)
    if 'Ceiling Plan' in sel_action:
        AddPrefixtoviews(doc, CeilingPlan)
    if 'Detail View' in sel_action:
        AddPrefixtoAnnotation(doc)
    if 'Drafting View' in sel_action:
        AddPrefixtoDimension(doc)
    if 'Elevation' in sel_action:
        AddPrefixtoAnnotation(doc)
    if 'Engineering Plan' in sel_action:
        AddPrefixtoDimension(doc)
    if 'Floor Plan' in sel_action:
        AddPrefixtoAnnotation(doc)
    if 'Legend' in sel_action:
        AddPrefixtoDimension(doc)
    if 'Rendering' in sel_action:
        AddPrefixtoAnnotation(doc)
    if 'Section' in sel_action:
        AddPrefixtoDimension(doc)
    if '3D View' in sel_action:
        AddPrefixtoAnnotation(doc)
    if 'Walk through' in sel_action:
        AddPrefixtoDimension(doc)
    else:
        pass
t.Commit()