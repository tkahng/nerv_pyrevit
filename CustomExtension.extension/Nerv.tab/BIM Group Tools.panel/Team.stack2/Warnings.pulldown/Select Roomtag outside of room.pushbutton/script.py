from pyrevit import revit, DB
doc = __revit__.ActiveUIDocument.Document

__doc__ = 'Select the Elements from Roomtag '\
          'outside of the Room Warning.'
# Find Warnings

warnings = doc.GetWarnings()
# Filter Warnings

selSet = []
count = 0
failingText = ''
for warning in warnings:
    message = warning.GetDescriptionText()
    elements = warning.GetFailingElements()
    failingText = 'Room Tag is outside of its Room'
    if failingText in message and count < 200:
        for element in elements:
            selSet.append(element)
            count += 1
print(str(len(selSet)) + ' < ' + failingText + ' >' + ' Elements were selected.')
# select Room Tags
revit.get_selection().set_to(selSet)
