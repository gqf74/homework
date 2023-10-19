import cv2 
import numpy as np
#impoert natplotlib.pylot 
#print(cv2.getVersionString())
image =cv2.imread("D:\work2.png")      #加载图像
#cv2.imshow("image",image)
b,g,r=cv2.split(image)   #分离图像色彩通道
#b,g,r=image[6,40]          #获得单个像素的像素值
#image_corner=image[0:50,0:50]            #获得图像内的某块区域
img_matplotlib=cv2.merge([r,g,b])       #调换通道顺序，存储反色图像

gray_image=cv2.imread("D:\work2.png",cv2.IMREAD_GRAYSCALE) 
gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)       #灰度访问图像
#i=gray_image[6,40]        #访问像素强度（不再有rgb），黑色强度值为0
ret,binary=cv2.threshold(gray_image,100,255,cv2.THRESH_BINARY)     #二值化图像，并返回执行结果+图片
cv2.imshow("binary",binary)
contours,hierarchy=cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    #查找轮廓与层级
cv2.drawContours(image,contours,-1,(0,255,255),1)   #绘制轮廓
cv2.imshow("image",image)
approx=cv2.approxPolyDP(contours[1],10,True)
cv2.drawContours(image,[approx],-1,(255,255,0),2)
cv2.imshow("image2",image)
cv2.waitKey(0)            #键盘绑定，等待按下任意键后执行
cv2.destroyAllWindows()         #关闭并释放所有窗口


colors={"blue":(255,0,0),"green":(0,255,0),"red":(0,0,255),"cyan":(255,255,0),"magenta":(255,0,255),"yellow":(0,255,255),"black":(0,0,0),"white":(255,255,255),"gray":(125,125,125),"dark_gray":(50,50,50),"light_gray":(220,220,220)}
#常见色彩RGB值

#img=cv2.rectangle(image,pt1,pt2,colors,thickness=1,lineType=8,shift=0)         #绘制正方形
#img=cv2.circle(image,center,radius,colors,thickness=1,lineType=8,shift=0)       #绘制圆形
#img=cv2.polylines(img,pts,isClosed,colors,thickness=1,lineType=8,shift=0)         #绘制多边形



#img_concats=np.concatenate((image,img_matplotlib),axis=0)       #合并显示原图和改图（axis为1是竖直边贴合，0为水平边）（只能合并相同通道数量的图）
#cv2.imshow("image,comnination",img_concats)      #显示图像（窗口名+显示的目标图像）
cv2.waitKey(0)            #键盘绑定，等待按下任意键后执行
cv2.destroyAllWindows()         #关闭并释放所有窗口

dimensions=image.shape   #图像行、列和通道的数量（彩图）
total_number_of_elements=image.size     #图像大小（高度、宽度、通道数）
image_dtype=image.dtype       #图像数据类型
#print(dimensions)