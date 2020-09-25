"""Add selected view to selected sheets."""

from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script


__author__ = 'Martin Lou'
__doc__ = 'Select all views from selected sheets.'


logger = script.get_logger()

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


dest_sheets = forms.select_sheets()
all_Viewport = []
if dest_sheets:
    logger.debug('Selected sheets: {}'.format(len(dest_sheets)))

    for sheet in dest_sheets:
        views = sheet.GetAllViewports()
        if views:
            for view in views:
                all_Viewport.append(view)
        else:
            pass
    revit.get_selection().set_to(all_Viewport)
else:
    forms.alert('No sheetss selected.')
