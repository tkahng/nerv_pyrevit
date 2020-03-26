import os

path = 'W:\Tools\Repo\pyRevit_custom_STV\CustomExtension.extension\\Nerv.tab'

for i, j, y in os.walk(path):
    if i[-5:] == 'panel':
        print(i)
