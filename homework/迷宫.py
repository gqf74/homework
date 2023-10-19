import sys
sys.setrecursionlimit(1000000)    #设置递归深度

import random
def maze_build():
    maze=[[0 for j in range(10)]for i in range(10)] #创立10*10的二维数组表示迷宫
    f=True
    while(f) :    #为什么是1？感觉会死循环啊。所以改成了一个指针，不知道行不行
        entrance=random.choice([(0, i) for i in range(1, 9)] + [(i, 0) for i in range(1, 9)] + [(i, 9) for i in range(1, 9)])  #任意选择三条边中的一边并在其上建立入口
        exit=random.choice([(0, i) for i in range(1, 9)] + [(i, 0) for i in range(1, 9)] + [(i, 9) for i in range(1, 9)])
        if (entrance[0]!=exit[0] and entrance [1]!= exit[1]):   #对比出入口的横纵坐标不同
            maze[entrance[0]][entrance[1]]="2"    #通过坐标访问入口位置并赋值
            maze[exit[0]][exit[1]]="8"
            f=False
        else:
            f=True
    for i in range(1,9):
          for j in range(1,9):
                maze[i][j]=str(random.randint(0,1))   #随机生成迷宫内容
    for i in range(0,10):    #想用■表示墙，看起来更清楚一些
          for j in range(0,10):            
                if maze[i][j]=="0" or maze[i][j]==0:
                    maze[i][j]="■"
    return maze,entrance,exit

def valid(maze,x,y):   #设置判断坐标有效性的函数
    if(x>=0 and x<len(maze) and y>=0 and y<len(maze[0]) and (maze[x][y]=="1" or "2")):
        return True
    else:
        return False
      
def try_walk(maze,x,y):     #验证迷宫可行性
    if valid(maze,x,y):
        if (maze[x][y]=="8"):
            print("迷宫可行")
    return True

def try_maze(maze,x,y,f):
        i=0
    #f=valid(maze,x,y)
    #if f :
        while i <100:         #尝试用递归验证迷宫是否可行...但是不知道怎么能保持同时试探四个方向
            if maze[x][y]=="8":   
                print("迷宫可行")
                return maze,x,y,f
            else:         #而且这个部分老是递归死循环，不知道为什么，试着用i限制递归次数好像也不行
                if valid(maze,x-1,y):
                    try_maze(maze,x-1,y,f)
                    i+=1
                if valid(maze,x,y-1):
                    try_maze(maze,x,y-1,f)
                    i+=1
                if valid(maze,x+1,y):
                    try_maze(maze,x+1,y,f)
                    i+=1
                if valid(maze,x,y+1):
                    try_maze(maze,x,y+1,f)
                    i+=1
                else:
                    print("迷宫不可行")
                    return maze,x,y,f
        #print("迷宫不可行")
        #return maze,x,y,f
            
            
build=maze_build()
maze,entrance,exit=build
x=entrance[0]
y=entrance[1]
#f=valid(maze,x,y)    #因为尝试调用检测函数会死循环所以暂时注释掉了
#tryresult=try_maze(maze,x,y,f)
maze,x,y,f=tryresult
if f:
    for i in range(10):  
        print(maze[i])
    while (maze[x][y]!="8"):
        maze[x][y]="3"   #做标记防止折回
        m=input("请输入移动方位：")
        if (m=="W"):
            x=x-1
        if (m=="A"):
            y=y-1
        if (m=="S"):
            x=x+1
        if (m=="D"):
            y=y+1
        if (maze[x][y]=="8"):
            print("恭喜走出迷宫！")
            break
        t=valid(maze,x,y)   #不知道为什么明明加了检测但是每次还是能破墙而出...
        if t:
            maze[x][y]="5"   #移动至新的位置
        else:
            print("遇到障碍物")   #很抱歉只会傻傻撤回...
            if (m=="W"):
                x=x-1
            if (m=="A"):
                y=y+1
            if (m=="S"):
                x=x+1
            if (m=="D"):
                y=y-1
        for i in range(10):
            print(maze[i])

#else:        #不知道怎么写能让它自动刷新迷宫并再次进入检测环节
    #build=maze_build()
    #maze,entrance,exit=build
    #x=entrance[0]
    #y=entrance[1]
    #tryresult=try_maze(maze,x,y,f)
    #maze,x,y,f=tryresult