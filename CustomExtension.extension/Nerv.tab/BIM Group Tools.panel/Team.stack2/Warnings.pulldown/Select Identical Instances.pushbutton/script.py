from pyrevit import revit, DB
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Select one of the Identical instance '\
          'that belong to the warning'
# Find Warnings

warnings = doc.GetWarnings()
# Filter Warnings

selSet = []
failingText = ""
for warning in warnings:
    message = warning.GetDescriptionText()
    elements = warning.GetFailingElements()
    failingText = 'identical instances'
    if failingText in message.lower():
        for element in elements:
            selSet.append(element)
            break

print(str(failingText + ' >' + ' Elements were selected.'))
# select Room Tags
revit.get_selection().set_to(selSet)
