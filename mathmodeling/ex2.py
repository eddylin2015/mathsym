# ——————01 调用包——————————
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import random


# ——————02 调参区—————————
w = 7         # 宽度
L = 33        # 长度
Lw = 4        # 等待区长度
dx = 10       # 点的大小
sjb = 1200     # 最大时间步长
sxtime = 0.01 # 刷新时间

# 函数：绘制网格线
def plot_line():
    # 绘制网格线
    q = range(1,L + 1)
    plt.xticks(range(1,L + 1,1),q)
    plt.xlim(0.5,L + 0.5)
    plt.ylim(0.5,w + 0.5)
    for i in range(1,L):
        x = [i+0.5,i+0.5]
        y = [0.5,w + 0.5]
        plt.plot(x,y,'-k',linewidth = 0.5)
    for j in range(1,w):
        x = [0.5,L + 0.5]
        y = [j+0.5,j+0.5]
        plt.plot(x,y,'-k',linewidth = 0.5)
    
    # 绘制分割线
    y= [Lw + 0.5,Lw + 0.5]
    x = [0.5,L + 0.5]
    #x = [Lw + 0.5,Lw + 0.5]
    #y = [0.5,w + 0.5]
    plt.plot(x,y,'-g',linewidth = 2)

    y = [w-Lw + 0.5,w-Lw + 0.5]
    x = [0.5,L + 0.5]
    #x = [L - Lw + 0.5,L - Lw + 0.5]
    #y = [0.5,w + 0.5]
    plt.plot(x,y,'-g',linewidth = 2)
    # 设置坐标刻度
    
    xz = range(1,L + 1) 
    plt.xticks(range(1,L + 1,1),xz)   # 横坐标刻度是整数
    #yz = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T']
    #plt.yticks(range(1,w + 1,1),yz)   # 纵坐标刻度是字母



# ——————03 创建图像————————
def poltPic(x1,y1,ob):
    plt.xlim(0.5,L + 0.5)
    plt.ylim(0.5,w + 0.5)
    plt.plot(x1,y1,ob,markersize = dx)
    


fig = plt.figure(figsize = (20,3.4))
ax = plt.axes()

# ——————04 随机生成初始元胞——————————
pessenger_ticket=list(range(1,199))
random.shuffle(pessenger_ticket)
pessenger_list=[]
for i in range(199):
    _x = int((pessenger_ticket[i-1]-1) / 6+1 )
    _y = int((pessenger_ticket[i-1]-1) % 6+1 )
    if _y>3 : _y = 1 + _y
    pessenger_list.append({"ticket":pessenger_ticket[i-1], "seat_x" :_x, "seat_y" :_y,"x":0,"y":4,})
    pass

#————————05 开始时间步循环—————————————
# 集合时间
sssj = 0
for m in range(sjb):
    sssj +=1
    # CA过程
    adjust_move_step=sssj if  sssj < len(pessenger_list) else len(pessenger_list)
    for i in range(adjust_move_step):
        _p=pessenger_list[i]
        if _p["seat_x"]==_p["x"] and _p["seat_y"]==_p["y"]:
            pass
        elif _p["x"]>=_p["seat_x"]:
            _p["x"]=_p["seat_x"] 
            _p["y"]=_p["seat_y"]
        else:
            _p["x"]+=1
        
    # 循环中绘制   
    x1 = []
    y1 = []
    for i,_p in enumerate(pessenger_list):
        if _p["x"]>0 and _p["seat_y"]<4:
            x1.append(_p["x"])
            y1.append(_p["y"])
    poltPic(x1,y1,'ob')
    x1 = []
    y1 = []
    for i,_p in enumerate(pessenger_list):
        if _p["x"]>0 and _p["seat_y"]>4:
            x1.append(_p["x"])
            y1.append(_p["y"])
    poltPic(x1,y1,'or')
    plot_line()
    plt.pause(sxtime)
    plt.cla()
    # 判断停止时间
    next_run=False
    for i,_p in enumerate(pessenger_list):
        if _p["seat_x"]==_p["x"] and _p["seat_y"]==_p["y"]:
            pass
        else:
            next_run=True
            break
    if not next_run: break

print("集合用时：" + str(sssj))

# 显示图片
#plt.show()

