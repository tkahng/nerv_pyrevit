import os
import shutil

path = 'W:\Tools\Repo\pyRevit_custom_STV\CustomExtension.extension\\Nerv.tab'
docPath = 'W:\\Tools\\Repo\pyRevit_custom_STV\\docs\\nerv'

index = "\n\
===========================\n\
\n\
Description\n\
\n\
.. toctree::\n\
   :maxdepth: 1\n\
   :name: "

buttonTemplate = "\n\
*********************\n\
\n\
.. figure:: {0}\n\
   :align: left\n\
\n\
   "

print(buttonTemplate.format('saidjwijd'))

masterFileAdd = open("W:\Tools\Repo\pyRevit_custom_STV\docs\index.rst", "a+")
masterFileRead = open("W:\Tools\Repo\pyRevit_custom_STV\docs\index.rst", "r").read()
# print(masterFileRead)
for i, j, y in os.walk(path):
    if i[-5:] == 'panel':
        # sprint(j)
        dir = os.path.join(docPath, os.path.basename(i[:-6]).replace(' ', '_').lower())
        # print(dir)

        # Make directory of a panel and create an index file
        if not os.path.exists(dir):
            os.mkdir(dir)
        if not os.path.exists(dir + "\\_static"):
            os.mkdir(dir + "\\_static")
        if not os.path.isfile(dir + "\\index.rst"):
            f = open(dir + "\\index.rst", "w")
            f.write(os.path.basename(i[:-6]).replace(' ', '_').lower() + index + 'nerv-' + os.path.basename(i[:-6]).replace(' ', '_').lower() + "\n")
            f.close()

        else:
            # print(os.path.basename(i[:-6]).replace(' ', '_').lower() + " panel index already exists")
            pass

        # Make the directory of a panel in mater index file
        pathText = "nerv/{0}/index.rst".format(os.path.basename(i[:-6]).replace(' ', '_').lower())
        if not pathText in str(masterFileRead):
            masterFileAdd.write("\n    " + pathText)
            # print("Path " + pathText + "added in Master index")
        else:
            # print("Path " + pathText + " already exists in Master index")
            pass

        # make pushbutton .rst for each push button
        for item in j:
            if ".pushbutton" in item:
                # if not os.path.isfile(dir + "\\" + item[:-11] + ".rst"):
                imageDis = dir + "\\" + "_static" + "\\" + item[:-11].replace(' ', '_').lower() + ".png"
                shutil.copy(i + '\\' + item + "\\" + "icon.png", imageDis)
                pushButtonFile = open(dir + "\\" + item[:-11].replace(' ', '_').lower() + ".rst", "w")
                pushButtonFile.write(item[:-11] + buttonTemplate.format("_static" + "/" + item[:-11].replace(' ', '_').lower() + ".png") + item[:-11].replace(' ', '_').lower())
                pushButtonFile.close()
                panelIndex = open(dir + "\\index.rst", "a+")
                panelIndexRead = open(dir + "\\index.rst", "r").read()
                if not item[:-11].replace(' ', '_').lower() in panelIndexRead:
                    panelIndex.write("\n   " + item[:-11].replace(' ', '_').lower())
            else:
                subName = item.split(".")[0].replace(' ', '_').lower()
                if not os.path.exists(dir + "\\" + subName):
                    os.mkdir(dir + "\\" + subName)


