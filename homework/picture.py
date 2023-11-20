import cv2
from cv_bridge import CvBridge 
import numpy as np
from std_msgs.msg import Header  # 载入msg类型
from sensor_msgs.msg import Image
import rospy
import rclpy
from rclpy.node import Node
#msg类型在命令行里用 ros2 interface package std_msgs查看(图片类型是Image?)
 
class publisher(Node):    #创建类
    def __init__(self, name, topic):     # 初始化name和topic(实例属性，self起头)
        super().__init__(name)
        # 创建发布节点
        self.publisher = self.create_publisher(Image, topic, 10)    #三个参数：(方法类型,话题名称,队列长度)
        self.get_logger().info("I'm publisher %s, I have topic '%s'" % (name, topic))
       
def main(args=None):
    height = 480
    width =  640
    image =cv2.imread(r"D:\1.jpg")      #加载图像
    cv2.imshow("image",image)
    #这里opencv的图像大小与ros发布的图像大小一致
    image.set(cv2.CAP_PROP_FRAME_WIDTH, width)    
    image.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    image.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))  

    # 初始化rclpy
    rclpy.init(args=args)
    #通过上方定义的类来实例化创建发布节点
    node = publisher(name='publish_node', topic='image_data')
    # 循环,保持节点运行
    rclpy.spin(node)
 
    bridge = CvBridge() # 转换为ros2的消息类型(imgmsg)的工具
 
    while True:       
        ret, frame = image.read()        
        frame = np.array(cv2.flip(frame,1))   # 镜像操作,且转为numpy.array   
        # 转换为ros2消息类型，且解码方式为b(blue)、g(green)、r(red)        
        data = bridge.cv2_to_imgmsg(frame,encoding="bgr8") 
        node.publish(data) # 发布转换好的图像类型消息
