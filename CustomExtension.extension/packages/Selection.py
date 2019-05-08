# Get all the elements
def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)

# get all parameters as dictionary with names nad values
def get_all_parameters_as_dic(element):
    '''
    Get a Dictionary of all element name, value and parameter object
    :param element:
    :return: dictionary
    '''
    parameters = element.Parameters
    _param = {}
    for param in parameters:
        if param:
            name = param.Definition.Name
            if 'String' in str(param.StorageType):
                try:
                    _param[name + ': ' +     str(param.AsString())] = param
                except:
                    _param[name + ': '+ str(param.AsValueString())] = param
            elif 'Interger' in str(param.StorageType):
                _param[name + ': ' + str(param.AsInterger())] = param
            elif 'Double' in str(param.StorageType):
                _param[name + ': ' + str(param.AsDouble())] = param
            elif 'ElementId' in str(param.StorageType):
                _param[name + ': '+ str(param.AsElementId().IntegerValue)] = param
    return _param

