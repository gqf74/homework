import cv2 
import numpy as np 

image =cv2.imread(r"D:\3102.jpg")      #加载图像
cv2.imshow("image",image)

#内参矩阵 
mtx=np.array([[1760.55506985705,0,646.283116140709],
             [0,1761.01541011471,483.376617258825],
             [ 0,0,1]],
              dtype=np.double),
#畸变矩阵
dist=np.array([[-0.0759322899962658,0.371617154476779,0,0,0]],dtype=np.double)

w=10
h=10
objp = np.zeros((w*h, 3), np.float32)  # 构造0矩阵，w*h行3列，用于存放角点的世界坐标
objp[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)  # 三维网格坐标划分

# 储存角点的世界坐标和图像坐标对
objpoints = []  # 在世界坐标系中的三维点（但是不知道到底是怎么收集并存储的）
imgpoints = []  # 在图像平面的二维点

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_float32=np.float32(gray)  #数据类型转换为float32

for fname in image:
    #检测角点
    corners=cv2.cornerHarris(gray_float32,2,3,0.04)  
    R=corners.max()*0.001  #设置阈值
    image[corners>R]=[0,255,225]     #标注角点
    # 如果找到点对，将其存储
    objpoints.append(objp)
    imgpoints.append(corners)
    # 将角点在图像上显示
cv2.imshow('findCorners', image)
cv2.waitKey()
cv2.destroyAllWindows()
 
ret=True
if ret:
    result,R,T=cv2.solvePnP(objpoints,imgpoints,mtx,dist)

print("旋转向量",R)
print("平移向量",T)
