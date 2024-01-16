#ifndef INFERENCE_H
#define INFERENCE_H

// Cpp native
#include <fstream>
#include <vector>
#include <string>
#include <random>

// OpenCV / DNN / Inference
#include <opencv2/imgproc.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>

//struct自定义类型收集这几个要素，要用的时候就通过加.访问，比如Detection detection
//也就是说通过detection这个值存储了推理结果的几个关键要素？
struct Detection
{
    int class_id{0};
    std::string className{};
    float confidence{0.0};
    cv::Scalar color{};
    cv::Rect box{};
};

class Inference
{
public:
    Inference(const std::string &onnxModelPath, const cv::Size &modelInputShape = {640, 640}, const std::string &classesTxtFile = "", const bool &runWithCuda = true);
    //关键字const用来定义常量，如果一个变量被const修饰，那么它的值就不能再被改变
    std::vector<Detection> runInference(const cv::Mat &input);

private:
    void loadClassesFromFile();
    void loadOnnxNetwork();
    cv::Mat formatToSquare(const cv::Mat &source);

    std::string modelPath{};
    std::string classesPath{};
    bool cudaEnabled{};

    std::vector<std::string> classes{"B1","B2","B3","B4","B5","B7","R1","R2","R3","R4","R5","R7"};
    //classes也要记得改（
    
    cv::Size2f modelShape{};
    //cv::Size2f sz( w, h ),32位浮点型size
    //size类不支持强制转换为固定向量类（cv::Vec）
    
    //设置判断阈值
    float modelConfidenceThreshold {0.25};
    float modelScoreThreshold      {0.45};
    //score：置信度的阈值，删除小于阈值的候选框
    float modelNMSThreshold        {0.50};

    bool letterBoxForSquare = true;
    //letterbox自适应图片缩放技术
    //train中放入的图片并不经过letterbox，而是在检测的时候使用

    cv::dnn::Net net;
};

#endif // INFE
