#1.1  File List:  *-*.jpg
from os import listdir
mypath = "./in/"
files = listdir(mypath)
cate={}
for f in files:
    if ".jpg" in f  or '.png' in f:
        print(f)
