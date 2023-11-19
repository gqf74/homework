#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
 
bridge = CvBridge() # 转换为ros2的消息类型(imgmsg)的工具
 
class subscriber(Node):    #创建类
    def __init__(self, name, topic):     # 初始化name和topic(实例属性，self起头)
        super().__init__(name)
        # 创建订阅节点
        self.subscriber= self.create_subscription(Image, topic, 10)    #三个参数：(方法类型,话题名称,队列长度)
        self.get_logger().info(" I'm subscriber %s, I get topic '%s'" % (name, topic))
        # 创建定时器
        timer_period=5.0
        self.timer = self.create_timer(timer_period, self.timer_callback)   #(时间周期，调用函数）每秒调用一次time_callback函数
 
    def callback(self,data):
        global bridge
        # ros2消息类型(imgmsg)转换为np.array
        cv_img = bridge.imgmsg_to_cv2(data, "bgr8") 
       
        cv2.imshow("" , cv_img) # 显示接受到的图像数据
        cv2.waitKey()
 
 
def main(args=None):
    rclpy.init()
    subnode =subscriber(name='subscribe_node', topic='image_data') # 实例化创建一个节点,定义其中的消息类型为Image。利用callback函数持续接收
    
    rclpy.spin(subnode)
    rclpy.shutdown()