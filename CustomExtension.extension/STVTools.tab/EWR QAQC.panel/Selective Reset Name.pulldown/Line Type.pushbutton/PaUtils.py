from Autodesk.Revit.DB import BuiltInCategory, GraphicsStyleType, Document, FilteredElementCollector, Line



def LineTypeCollector(doc):
    lines = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
    out = []
    for i in lines:
        PAlineStyle = []

        if i.Name[0:5] == 'PA - ':
            PAlineStyle.append(i.Name)
            PAlineStyle.append(i.LineColor.Red)
            PAlineStyle.append(i.LineColor.Green)
            PAlineStyle.append(i.LineColor.Blue)
            PAlineStyle.append(i.GetLineWeight(GraphicsStyleType.Projection))
            pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
            if pattern is None:
                PAlineStyle.append('Solid')
            else:
                PAlineStyle.append(pattern.Name)
            out.append(PAlineStyle)
    return out

def AltLineTypeCollector(doc):
    lines = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines).SubCategories
    out = []
    for i in lines:
        PAlineStyle = []

        if i.Name[0:5] != 'PA - ':
            PAlineStyle.append(i.Name)
            PAlineStyle.append(i.LineColor.Red)
            PAlineStyle.append(i.LineColor.Green)
            PAlineStyle.append(i.LineColor.Blue)
            PAlineStyle.append(i.GetLineWeight(GraphicsStyleType.Projection))
            pattern = doc.GetElement(i.GetLinePatternId(GraphicsStyleType.Projection))
            if pattern is None:
                PAlineStyle.append('Solid')
            else:
                PAlineStyle.append(pattern.Name)
            out.append(PAlineStyle)
    return out

def LineCollector(doc):
    lineInstance = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Lines).ToElements()
    print(lineInstance)

def