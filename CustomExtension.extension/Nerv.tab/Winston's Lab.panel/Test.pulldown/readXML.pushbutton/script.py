import bs4
from bs4 import BeautifulSoup
# Documentation of work
points = {}
file = "C:\\Users\\mengf\\Desktop\\C1152UUMST02C19.xml"
with open(file, "r") as f:
    # Read each line in the file, readlines() returns a list of lines
    content = f.readlines()
    # Combine the lines in the list into a string
    content = "".join(content)
    bs_content = bs4.BeautifulSoup(content, "html.parser")

    struct= bs_content.find_all("struct")

    for a in struct:
        try:
            print(a.attrs['name'])
            print(a.find("center").text).split(" ")
            print(a.find("invert").attrs['elev'] + str("0"))
        except:
            pass
# find pipe
    pipes = bs_content.find_all("pipe")

    for a in pipes:
        if a.find("circpipe"):
            print(str(a.find("circpipe").attrs['diameter']) + str("0"))
        if a.find("rectpipe"):
            print(str(a.find("rectpipe").attrs['width']) + str("0"))
            print(str(a.find("rectpipe").attrs['height']) + str("0"))
        print(a.attrs['name'])
        print(a.attrs['refend'])
        print(a.attrs['refstart'])



