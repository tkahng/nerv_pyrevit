from pyrevit import revit, DB
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Select the Room not in enclosed region based on model warning.'
# Find Warnings

warnings = doc.GetWarnings()
# Filter Warnings

selSet = []
count = 0
failingText = ''
for warning in warnings:
    message = warning.GetDescriptionText()
    elements = warning.GetFailingElements()
    failingText = 'Room is not in a properly enclosed region'
    if failingText in str(message) and count < 51:
        for element in elements:
            selSet.append(element)
            count += 1
print(str(len(selSet)) + ' < ' + failingText + ' >' + ' Elements were selected.')
# select Room Tags
revit.get_selection().set_to(selSet)
