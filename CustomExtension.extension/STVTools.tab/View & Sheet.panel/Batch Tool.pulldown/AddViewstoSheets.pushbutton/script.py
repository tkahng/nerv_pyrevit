"""Add selected view to selected sheets."""

from pyrevit import revit, DB
from pyrevit import forms
from pyrevit import script
from Autodesk.Revit.DB import BuiltInParameter

__author__ = 'Dan Mapes Modified by Martin Lou'
__doc__ = 'Adds the selected views (callouts, sections, elevations) to the '\
          'selected sheets. Model views will only be added to the first '\
          'selected sheet since they can not exist on multiple sheets. ' \
          'The command defaults to active view if no views are selected.' \
          '\n\nShift+Click:\n' \
          'Pick source views from list instead of selection or active view.'

logger = script.get_logger()

selected_views = []


if __shiftclick__:
    selected_views = forms.select_views()
else:
    # get selection and verify a view is selected
    selection = revit.get_selection()
    if not selection.is_empty:
        logger.debug('Getting views from selection.')
        for el in selection:
            if el.Category and el.Category.Name == 'Views':
                logger.debug('Selected element referencing: {}'
                             .format(el.Name))
                target_view = revit.query.get_view_by_name(el.Name)
                if target_view:
                    logger.debug('Target view: {}'
                                 .format(revit.query.get_name(target_view)))
                    selected_views.append(target_view)
    else:
        selected_view = revit.activeview
        if not isinstance(selected_view, DB.View):
            forms.alert('Active view must be placable on a sheet.', exitscript=True)
        logger.debug('Selected view: {}'.format(selected_view))
        selected_views = [selected_view]


if selected_views:
    logger.debug('Selected views: {}'.format(len(selected_views)))
    # get the destination sheets from user
    dest_sheets = forms.select_sheets()
    all_Viewport = []
    if dest_sheets:
        logger.debug('Selected sheets: {}'.format(len(dest_sheets)))
        with revit.Transaction("Add Views to Sheets"):
            if len(selected_views) != len(dest_sheets):
                print('view selection number does not match sheet selection number')
            else:
                count = 0
                for selected_view in selected_views:
                    logger.debug('Adding: %s',
                                 revit.query.get_name(selected_view))
                    try:
                        viewport = DB.Viewport.Create(revit.doc,
                                           dest_sheets[count].Id,
                                           selected_view.Id,
                                           DB.XYZ(17, 11, 0))
                        all_Viewport.append(viewport)
                    except Exception as place_err:
                        print('Error placing view on sheet: {} -> {}'
                                     .format(selected_view.Id, dest_sheets[count].Id))
                    count += 1
    revit.get_selection().set_to(all_Viewport)
else:
    forms.alert('No views selected.')
