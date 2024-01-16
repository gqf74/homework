#include <iostream>
//头文件，给予使用部分功能的权限 
#include <vector>
//#include <getopt.h>

#include <opencv2/opencv.hpp>
//opencv.hpp包含了常用的头文件

#include "inference.h"

using namespace std;
//为了解决命名冲突的问题而引入的概念 
//C＋＋标准程序库中的所有标识符都被定义于一个名为std的namespace中
using namespace cv;
//OpenCV的函数都位于cv这一命名空间下,调用OpenCV的函数，需要在每个函数前加上cv::
//(就相当于python中的import?)

int main(int argc, char **argv)
//main函数，每一个C++程序都需要有一个main函数 
{
    bool runOnGPU = true;
    // 1.设置onnx模型
    //此处的类是硬编码（把一个本来应该（可以）写到配置信息中的信息直接在程序代码中写死）
    //“classes.txt”是一个占位符
    Inference inf("/home/gqf74/yolov8/Model deployment/Model deployment and picture/code/model/weights/best.onnx", cv::Size(480,640), "classes.txt", runOnGPU); 
    // 2.设置输入图片
    std::vector<std::string> imageNames;
    //与arrays一样，vector 对元素使用连续的存储位置，但与arrays不同，它们的大小可以动态变化
    //其实结构就是vector<string> imageNames，创建格式为vector<数据类型> 名字
    imageNames.push_back("/home/gqf74/yolov8/Model deployment/Model deployment and picture/code/source/000601.jpg");  
    //在对象imageNames中添加内容
    //imageNames.push_back("zidane.jpg");
    

    for (int i = 0; i < imageNames.size(); ++i)  //size()函数获得Vectorc的大小
    {
        cv::Mat frame = cv::imread(imageNames[i]);
        //cv::Mat用于表示任意维度的稠密数组，OpenCV使用它来存储和传递图像
        //它里面的元素可以是“像素”（基本数据类型+通道数）

        // 开始推理
        std::vector<Detection> output = inf.runInference(frame);
        //把runInference的结果放在符合detection格式的output中

        //输出一共有几个目标
        int detections = output.size();
        std::cout << "Number of detections:" << detections << std::endl;

        //调整图片大小方便展示结果（别忘了同步调整框的位置，就是取消框的缩放）
        //cv::resize(frame, frame, cv::Size(480,640),INTER_LINEAR);

        for (int i = 0; i < detections; ++i)
        //对于每一个结果(output[i])循环一次画出一个预测框
        {
            Detection detection = output[i];

            cv::Rect box = detection.box;
            //rect(左上x-坐标，左上y-坐标，宽，高)创建一个矩形对象

            cv::Scalar color = detection.color;
            //Scalar是一个由长度为4的数组作为元素构成的结构体
            //Scalar最多可以存储四个值，没有提供的值默认是0
            //用scalar来储存随机生成的框的bgr值

            cv::rectangle(frame, box, color, 2);
            // Detection box检测框
            //rectangle参数（输入图像、顶点、对角顶点、颜色、线条粗细）

            std::string classString = detection.className + ' ' + std::to_string(detection.confidence).substr(0, 4);
            // Detection box text检测框文本
            //substr(string,start<,length>):从string 的start位置开始提取length长度的字符串
            //std::to_string数值转换字符串，显示置信度和分类准确率计算出的正确率

            cv::Size textSize = cv::getTextSize(classString, cv::FONT_HERSHEY_DUPLEX, 1, 2, 0);
            //textSize设置文字大小
            //cv::FONT_HERSHEY_DUPLEX只是一种字体（？
            //cv::getTextSize()函数能够实现如果把文字绘制出来将有多大，而不用实际将文字绘制到图上
            
            cv::Rect textBox(box.x, box.y - 40, textSize.width + 10, textSize.height + 20);
            //画出完整带文字的识别框

            cv::rectangle(frame, textBox, color, cv::FILLED);
            cv::putText(frame, classString, cv::Point(box.x + 5, box.y - 10), cv::FONT_HERSHEY_DUPLEX, 1, cv::Scalar(0, 0, 0), 2, 0);
        }
        cv::imshow("Inference", frame);
        cv::waitKey(0);
        cv::destroyAllWindows();
    }
}

