import cv2 
import numpy as np 
#print(cv2.getVersionString())
image =cv2.imread("D:\work2.png")      #加载图像
b,g,r=cv2.split(image)   #分离图像色彩通道
#b,g,r=image[6,40]          #获得单个像素的像素值
#image_corner=image[0:50,0:50]            #获得图像内的某块区域
#img_matplotlib=cv2.merge([r,g,b])       #调换通道顺序，存储反色图像

gray_image=cv2.imread("D:\work2.png",cv2.IMREAD_GRAYSCALE) 
gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)       #灰度访问图像
#i=gray_image[6,40]        #访问像素强度（不再有rgb），黑色强度值为0
ret,binary=cv2.threshold(gray_image,100,255,cv2.THRESH_BINARY)     #阈值二值化图像，并返回执行结果+图片
cv2.imshow("binary",binary)
gs_binary=cv2.GaussianBlur(binary,(5,5),0)      #将图像进行高斯模糊方便提取
cv2.imshow("gs_binary",gs_binary)
erode_binary=cv2.erode(binary,None,iterations=2)     #腐蚀图像去除干扰，和高斯模糊对比了一下感觉腐蚀效果好一点
cv2.imshow("erode image",erode_binary)
contours,hierarchy=cv2.findContours(erode_binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    #查找轮廓与层级
for cnt in range(len(contours)):
    #cv2.drawContours(image,contours,cnt,(0,255,255),1)   #绘制轮廓
    epsilon=0.01*cv2.arcLength(contours[cnt],True)
    approx=cv2.approxPolyDP(contours[cnt],epsilon,True)   #多边形逼近
    corners=len(approx)               #分析几何形状,但是感觉只端点个数并无法完全判断图像几何形状、完全排除干扰
    shape_type=" "
    if corners==3:
        #count=self.shapes['triangle']
        shape_type="三角形"
        cv2.drawContours(image,[approx],-1,(0,255,255),2)
        print(shape_type)
    if 15>corners>10:
        shape_type="圆形"
        cv2.drawContours(image,[approx],-1,(0,255,255),2)
        print(shape_type)
cv2.imshow("image2",image)
cv2.waitKey(0)            #键盘绑定，等待按下任意键后执行
cv2.destroyAllWindows()         #关闭并释放所有窗口




#以下为学习内容请忽略
colors={"blue":(255,0,0),"green":(0,255,0),"red":(0,0,255),"cyan":(255,255,0),"magenta":(255,0,255),"yellow":(0,255,255),"black":(0,0,0),"white":(255,255,255),"gray":(125,125,125),"dark_gray":(50,50,50),"light_gray":(220,220,220)}
#常见色彩RGB值

#img=cv2.rectangle(image,pt1,pt2,colors,thickness=1,lineType=8,shift=0)         #绘制正方形
#img=cv2.circle(image,center,radius,colors,thickness=1,lineType=8,shift=0)       #绘制圆形
#img=cv2.polylines(img,pts,isClosed,colors,thickness=1,lineType=8,shift=0)         #绘制多边形

#img_concats=np.concatenate((image,img_matplotlib),axis=0)       #合并显示原图和改图（axis为1是竖直边贴合，0为水平边）（只能合并相同通道数量的图）
#cv2.imshow("image,comnination",img_concats)      #显示图像（窗口名+显示的目标图像）


dimensions=image.shape   #图像行、列和通道的数量（彩图）
total_number_of_elements=image.size     #图像大小（高度、宽度、通道数）
image_dtype=image.dtype       #图像数据类型
#print(dimensions)