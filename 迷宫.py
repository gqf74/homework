import random
def maze_build():
    maze=[[0 for j in range(10)]for i in range(10)]   #创立10*10的二维数组表示迷宫
    f=True
    while(f) :    #为什么是1？感觉会死循环啊。所以改成了一个指针，不知道行不行
        entrance=random.choice([(0, i) for i in range(1, 9)] + [(i, 0) for i in range(1, 9)] + [(i, 9) for i in range(1, 9)])  #任意选择三条边中的一边并在其上建立入口
        exit=random.choice([(0, i) for i in range(1, 9)] + [(i, 0) for i in range(1, 9)] + [(i, 9) for i in range(1, 9)])
        if (entrance[0]!=exit[0] and entrance [1]!= exit[1]):   #对比出入口的横纵坐标不同
            maze[entrance[0]][entrance[1]]=2     #通过坐标访问入口位置并赋值
            maze[exit[0]][exit[1]]=8
            f=False
        else:
            f=True
    for i in range(1,9):
          for j in range(1,9):
                maze[i][j]=random.randint(0,1)   #随机生成迷宫内容
    return maze,entrance,exit

def valid(maze,x,y):   #设置判断坐标有效性的函数
    if(x>=0 and x<len(maze) and y>=0 and y<len(maze[0]) and maze[x][x]==1):
        return True
    else:
         return False
      
def walk(maze,x ,y):     #移动并判断移动结果
    if valid(maze,x,y):
        while (maze[x][y]!=8):
            maze[x][y]=3   #做标记防止折回
            m=input("请输入移动方位：")
            if (m=="W"):
                x=x-1
            if (m=="A"):
                y=y-1
            if (m=="S"):
                x=x+1
            if (m=="D"):
                y=y+1
            if (maze[x][y]==8):
                break
            elif (valid(maze,x,y)):
                maze[x][y]=5   #移动至新的位置
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
                i+=1
    return maze

def try_walk(maze,x,y):
    if (maze[x][y]==8):
        print("迷宫可行")
        return True

build=maze_build()
maze,entrance,exit=build
#for i in range(10):   #测试一下输出迷宫阵列
    #print(maze[i])
    #i+=1
x=entrance[0]
y=entrance[1]
for i in range(100):    #尝试一下验证迷宫是否可行......
    maze[x][y]=3
    if try_walk(maze,x-1,y) or try_walk(maze,x,y-1) or try_walk(maze,x+1,y) or try_walk(maze,x,y+1):
        break
    else:
        build=maze_build()
        break
   
walk(maze,x,y)