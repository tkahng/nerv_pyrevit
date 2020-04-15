import bs4
from bs4 import BeautifulSoup
# Documentation of work
def GetUniqueClashfromHTML(row):
    list = []
    clashItems = ""
    clashItemsRev = ""
    item1 = ""
    item2 = ""
    text1 = row.find_all('td', class_='item1Content')
    count1 = 0
    for t in text1:
        if count1 < 2:
            item1 += t.get_text().replace(" ", "").replace("\n", "").replace("ElementID:", "").replace(
                "-FQ19144N-BL001.rvt", "")
            count1 += 1
        else:
            break
    text2 = row.find_all('td', class_='item2Content')
    count2 = 0
    for t in text2:
        if count2 < 2:
            item2 += t.get_text().replace(" ", "").replace("\n", "").replace("ElementID:", "").replace(
                "-FQ19144N-BL001.rvt", "")
            count2 += 1
        else:
            break
    if item1 and item2:
        clashItems += item1
        clashItems += item2
        clashItemsRev += item2
        clashItemsRev += item1
        list.append(clashItems)
        list.append(clashItemsRev)
    return list

file = "C:\\Users\\mengf\\Desktop\\C1152UUMST02C19.xml"
with open(file, "r") as f:
    # Read each line in the file, readlines() returns a list of lines
    content = f.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs4.BeautifulSoup(content, "html.parser")
# find point
    struct= bs_content.find_all("struct")

    for a in struct:
        print(a.attrs['name'])
# find pipe
    pipes = bs_content.find_all("pipe")

    for a in pipes:
        print(a.find("circpipe"))
        print(a.attrs['name'])
        print(a.attrs['refend'])
        print(a.attrs['refstart'])



