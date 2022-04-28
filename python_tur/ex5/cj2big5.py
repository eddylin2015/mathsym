ChnList="日月金木水火土竹戈十大中一弓人心手口尸廿山女田X卜Z"
EngLit="abcdefghijklmnopqrstuvwxyZ"
cjkeydic={}
for i in range(len(EngLit)):
    cjkeydic[EngLit[i]]=ChnList[i]
    

dic={}
with open('cj.txt',encoding="utf-8") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        row_=lines[i].split("\t")

        if len(row_)==2:
            try:
                if row_[1].startswith("z") or row_[1].startswith("yyy"):
                    pass
                else:
                    dic[row_[0]]=row_[1].replace("\n","")
            except:
                pass
count_chn=[]
with open('ori.txt',encoding="utf-8") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            chr=lines[i][j]
            if chr in dic:
                chnkey=""
                for k in range(len(dic[chr])):
                    chnkey=chnkey+cjkeydic[dic[chr][k]]
                if chr in count_chn :
                    pass
                else:
                    print([chr,chnkey])
                    count_chn.append(chr)

