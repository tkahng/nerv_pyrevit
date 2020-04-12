import re, os
import bs4, soupsieve
from pyrevit import forms

__doc__ = 'STV BIM button to read clash data off html and generate data files'

# Set the path with all the clash html files and the path of the output file that you want py revit to pick up
clashpath = '\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\90_CAD Models and Sheets\\' \
            '17017000\\_PIM\\' # ClashReportData\\'


approvedTail = ['ENC', 'FFE', 'GEN', 'INT', 'SSM', 'C', 'CP', 'PBB', ]

# Get File name
def FileName(dirpath):
    filenameLst = []
    for file in os.listdir(dirpath):
        filenameLst.append(file)
    return filenameLst


def Pickname(tailName, noTailName):
    if len(tailName) != 0:
        tailLst = re.split('_', tailName[0])
        if tailLst[2] in approvedTail:
            newfilename = tailName[0]
        else:
            newfilename = tailLst[0] + '_' + tailLst[1]
    else:
        newfilename = noTailName[0]
    return newfilename

clashFiles = forms.pick_file(file_ext='html', multi_file=True, init_dir=clashpath, unc_paths=False)
# get the name of the folder picked
pickedFilePath = os.path.dirname(clashFiles[0])
pickedFolder = os.path.basename(os.path.dirname(pickedFilePath))
print(pickedFolder)
folderName = str(forms.GetValueWindow.show(None,
        value_type='string',
        default=pickedFolder,
        prompt='Please Enter the Clash Report Name after the date.',
        title='Clash Report Name')) + '\\'
programPath = '\\\\stvgroup.stvinc.com\\v3\\DGPA\\Vol3\\Projects\\3019262\\3019262_0001\\' \
              '90_CAD Models and Sheets\\17017000\\_PIM\\PointData\\' + folderName

modelNameRegex = re.compile(r'\w\d\d\d\d\d\d\d\d-\S\S_CENTRAL\S{4}?')
modelRegex = re.compile(r'\w\d\d\d\d\d\d\d\d-\S\S_CENTRAL')
modelRegex2 = re.compile(r'\w\d\d\d\d\d\d\d\d-\S\S_CENTRAL_\w?\w?\w')
ElementIDRegex = re.compile(r'Element ID:\D+?\d+')
IDRegex = re.compile(r'\d+')
nameLst = []
for clashFile in clashFiles:
    nameLst.append(os.path.basename(clashFile))

xPntdata = []
yPntdata = []
zPntdata = []
lstLen = []
newfilename = ()
count = 0
print('We found ' + str(len(clashFiles)) + ' Clash Files.')
pb =  forms.ProgressBar(title='Files Processing')

# Write data
for filename in clashFiles:
    newFilename = nameLst[count]
    a = 0
    clashFile = open(filename)
    clashSoup = bs4.BeautifulSoup(clashFile, "html.parser")
    pnt = clashSoup.select('body')
    # Locate clash data
    clashData = pnt[0].getText()
    # Search for File name in Soup
    fileNames = modelNameRegex.findall(clashData)
    currentFile = fileNames[:: 2]
    otherFile = fileNames[1:: 2]
    # Search for element ID in Soup
    elementID = ElementIDRegex.findall(clashData)
    elementIDPool = []
    for i in elementID:
        elementIDP = str(IDRegex.findall(i))
        elementIDPool.append(elementIDP)
    currentID = elementIDPool[:: 2]
    otherID = elementIDPool[1:: 2]
    # Find x,y and z
    dataRegex = re.compile(r'\S?\d+.\d+')
    xRegex = re.compile(r'x:\S?\d+.\d+')
    yRegex = re.compile(r'y:\S?\d+.\d+')
    zRegex = re.compile(r'z:\S?\d+.\d+')
    xPnt = xRegex.findall(clashData)
    yPnt = yRegex.findall(clashData)
    zPnt = zRegex.findall(clashData)
    generalFilenames = modelNameRegex.findall(clashData)

    # Determine the file name

    if len(generalFilenames) != 0:
        foundFileNames = []
        firstName = generalFilenames[0]
        secondName = generalFilenames[1]
        print('First File name is ' + firstName)
        print('Second File name is ' + secondName)
        FnoTailName = modelRegex.findall(firstName)
        FtailName = modelRegex2.findall(firstName)
        SnoTailName = modelRegex.findall(secondName)
        StailName = modelRegex2.findall(secondName)
        # TODO: Save fix function
        foundFileNames.append(Pickname(FtailName, FnoTailName))
        foundFileNames.append(Pickname(StailName, SnoTailName))
    else:
        foundFileNames = ['Nodata', 'Nodata']

    for indiFileName in foundFileNames:
        xPntdata = []
        yPntdata = []
        zPntdata = []
        for x in xPnt:
            xList = re.split(':', x)
            xPntdata.append(xList[1])
        for y in yPnt:
            yList = re.split(':', y)
            yPntdata.append(yList[1])
        for z in zPnt:
            zList = re.split(':', z)
            zPntdata.append(zList[1])
        a = len(xPnt)
        lstLen.append(a)

        try:
            os.mkdir(programPath + indiFileName)
        except OSError:
            print("Creation of the directory %s failed" % programPath)
        else:
            print("Successfully created the directory %s " % programPath)
        print("---------------------------------------------------------------")
        pointFile = open(programPath + indiFileName + '\\' +
                         foundFileNames[0] + ' VS ' + foundFileNames[1] + ' Pointdata.py', 'w')
        '''
        pointFile.write('pointX = ' + pprint.pformat(xPntdata) + '\n')
        pointFile.write('pointY = ' + pprint.pformat(yPntdata) + '\n')
        pointFile.write('pointZ = ' + pprint.pformat(zPntdata) + '\n')
        if indiFileName == foundFileNames[0]:
            pointFile.write('clashName = ' + pprint.pformat(currentID) + '\n')
            pointFile.write('clashwithID= ' + pprint.pformat(otherID) + '\n')
        elif indiFileName == foundFileNames[1]:
            pointFile.write('clashName = ' + pprint.pformat(otherID) + '\n')
            pointFile.write('clashwithID= ' + pprint.pformat(currentID) + '\n')
        pointFile.write('currentFile = ' + pprint.pformat(currentFile) + '\n')
        pointFile.write('otherFile = ' + pprint.pformat(otherFile) + '\n')
        pointFile.write('lstlen = ' + pprint.pformat(lstLen) + '\n')
        '''
        pointFile.write('pointX = ' + str(xPntdata) + '\n')
        pointFile.write('pointY = ' + str(yPntdata) + '\n')
        pointFile.write('pointZ = ' + str(zPntdata) + '\n')
        if indiFileName == foundFileNames[0]:
            pointFile.write('clashName = ' + str(currentID) + '\n')
            pointFile.write('clashwithID= ' + str(otherID) + '\n')
        elif indiFileName == foundFileNames[1]:
            pointFile.write('clashName = ' + str(otherID) + '\n')
            pointFile.write('clashwithID= ' + str(currentID) + '\n')
        pointFile.write('currentFile = ' + str(currentFile) + '\n')
        pointFile.write('otherFile = ' + str(otherFile) + '\n')
        pointFile.write('lstlen = ' + str(lstLen) + '\n')
    pb.update_progress(count, len(clashFiles))
    count += 1
print("Finished!!!!!")