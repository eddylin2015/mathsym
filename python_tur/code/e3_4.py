files ="""1001-a.png
1001-b.jpeg
1001-c.jpg
21444-a.jpg
21444-b.jpg""".split("\n")

category={}
for f in files:
    if ".jpg" in f  and '-' in f:
        key , val =f.split('-')
        if key in category:
            category[key].append( f )
        else:
            category[key]=[f]
print(category)
