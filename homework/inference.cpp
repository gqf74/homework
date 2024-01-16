#include "inference.h"

//通过已定义的类Inference实例化对象Inference并赋予初始值
Inference::Inference(const std::string &onnxModelPath, const cv::Size &modelInputShape, const std::string &classesTxtFile, const bool &runWithCuda)
{
    modelPath = onnxModelPath;
    //model_path：已训练完成的模型，支持重新训练的模型
    modelShape = modelInputShape;
    classesPath = classesTxtFile;
    //classes_path：类别文件，与模型文件匹配
    cudaEnabled = runWithCuda;

    loadOnnxNetwork();
    // loadClassesFromFile(); The classes are hard-coded for this example，就是已经写在头文件里了
}

std::vector<Detection> Inference::runInference(const cv::Mat &input)
{
    //前处理（调整图像大小）
    cv::Mat modelInput = input;
    //用Mat存储输入的图片（此处为一个占位符？）
    if (letterBoxForSquare && modelShape.width == modelShape.height)
        modelInput = formatToSquare(modelInput);
        //转化为正方形（但是没调大小)
        //已经是正方形的话可以直接resize吗

    cv::Mat blob;
    //Mat是opencv这一领域的一种协议，它决定了在opencv中一副图片数据的存储顺序
    //Blob是caffe这一领域的一种协议，Blob分析就是对前景、背景分离后的二值图像，进行连通域提取和标记
    //每一个Blob都代表一个前景目标，然后就可以计算Blob的一些相关特征
    //但它们共有n（图片数量）、c（通道数）、w（宽度）、h（高度）这四个要素，并以此为转换桥梁
    cv::dnn::blobFromImage(modelInput, blob, 1.0/255.0, modelShape, cv::Scalar(), true, false);
    //DNN模块中的blobFromImge模块，将图片转换DNN模块能够读的格式
    //OpenCV中的深度学习模块（DNN）只提供了推理功能，不涉及模型的训练
    //DNN模块提供了内建的CPU和GPU加速，若项目中之前使用了OpenCV，那么通过DNN模块可以很方便的为原项目添加深度学习的能力
    net.setInput(blob);
    //往DNN中输入blob类型的图片

    //获得模型的输出（一个整个的数组数据）
    std::vector<cv::Mat> outputs;
    net.forward(outputs, net.getUnconnectedOutLayersNames());


    //数据预处理
    int rows = outputs[0].size[1];
    int dimensions = outputs[0].size[2];

    bool yolov8 = false;
    // yolov5 has an output of shape (batchSize, 25200, 85) (Num classes + box[x,y,w,h] + confidence[c])
    // yolov8 has an output of shape (batchSize, 84,  8400) (Num classes + box[x,y,w,h])
    //模型得到的输出格式为（84x8400），84=边界框预测值4+数据集类别80
    //8400是v8模型各尺度输出特征图叠加之后的结果
    if (dimensions > rows) // Check if the shape[2] is more than shape[1] (yolov8)
    {
        yolov8 = true;
        rows = outputs[0].size[2];
        dimensions = outputs[0].size[1];

        outputs[0] = outputs[0].reshape(1, dimensions);
        //8400个特征图的cell，每个cell里面有4+1+80的输出值，对应4个预测框特征点（xywh)+1个置信度（最大类别概率）+80类别概率
        cv::transpose(outputs[0], outputs[0]);
        //transpose函数的功能相当于矩阵的转置，即将矩阵沿着对角线进行翻转
        //方便下文data和classes存储xywh相关信息？
    }
    float *data = (float *)outputs[0].data;
    //C语言规定*a代表a中存储的地址对应的存储单元中的数据

    //原图变成标准640*640大小的缩放比例（处理后的/原来的）
    float x_factor = modelInput.cols / modelShape.width;
    float y_factor = modelInput.rows / modelShape.height;

    std::vector<int> class_ids;
    std::vector<float> confidences;
    std::vector<cv::Rect> boxes;
    

    for (int i = 0; i < rows; ++i)
    {
        // if (yolov8)
        {   
            //通过最大置信度筛选类别？
            //yolov8不另外对置信度预测， 而是采用类别里面最大的概率作为置信度score
            float *classes_scores = data+4;

            cv::Mat scores(1, classes.size(), CV_32FC1, classes_scores);
            //存储模型分类结果？
            //CV_32FC1:32位float数据类型，1通道
            cv::Point class_id;
            //cv::Point 类，它是一个由坐标 x 和 y 指定的 2D 点的模板类
            double maxClassScore;

            minMaxLoc(scores, 0, &maxClassScore, 0, &class_id);
            //找到scores中最大值的实际值与位置
            //minMaxLoc（）函数 是 OpenCV 库中的一个函数，用于找到一个多维数组中的最小值和最大值，以及它们的位置
            //(数组/向量，最小值的实际值（可设为0），最大值的实际值（可设为0），最小值的位置，最大值的位置，大小和类型必须与 src 相同的掩码)
            
            //std::cout << "b" << maxClassScore << std:: endl;
            if (maxClassScore > modelScoreThreshold) //通过设置阈值排除干扰可能项
            {
                confidences.push_back(maxClassScore);
                class_ids.push_back(class_id.x);

                float x = data[0];
                float y = data[1];
                float w = data[2];
                float h = data[3];

                //我们此时模型的输入是经过letterbox处理的，所以需要先将预测框的坐标转换回原坐标系的坐标
                //将xywh转换为左上角右下角坐标
                int left = int((x - 0.5 * w) * x_factor);
                int top = int((y - 0.5 * h) * y_factor);
                int width = int(w * x_factor);
                int height = int(h * y_factor);

                boxes.push_back(cv::Rect(left, top, width, height));
                //此时的定位是相对于原图坐标的定位？
            }
        }
        // else // yolov5
    //     {
    //         float confidence = data[4];

    //         if (confidence >= modelConfidenceThreshold)
    //         {
    //             float *classes_scores = data+5;

    //             cv::Mat scores(1, classes.size(), CV_32FC1, classes_scores);
    //             cv::Point class_id;
    //             double max_class_score;

    //             minMaxLoc(scores, 0, &max_class_score, 0, &class_id);

    //             if (max_class_score > modelScoreThreshold)
    //             {
    //                 confidences.push_back(confidence);
    //                 class_ids.push_back(class_id.x);

    //                 float x = data[0];
    //                 float y = data[1];
    //                 float w = data[2];
    //                 float h = data[3];

    //                 int left = int((x - 0.5 * w) * x_factor);
    //                 int top = int((y - 0.5 * h) * y_factor);

    //                 int width = int(w * x_factor);
    //                 int height = int(h * y_factor);

    //                 boxes.push_back(cv::Rect(left, top, width, height));
    //             }
    //         }
    //     }

        data += dimensions;
        //逐个获得检测框信息
    }


    //后处理（置信度过滤+NMS非极大值抑制）
    std::vector<int> nms_result;
    //std::cout << "boxes1: " << boxes[0] << boxes[1] << std::endl;
    cv::dnn::NMSBoxes(boxes, confidences, modelScoreThreshold, modelNMSThreshold, nms_result);
    //NMS:非极大值抑制，筛选预测框
    //首先根据_score_threshold过滤掉那些分数低于阈值的预测框
    //对剩下的预测框，如果它的周围有高于它的预测框，则将置信度更低的预测框抑制掉
    //保留那些没有被抑制的预测框，这些预测框的索引保存在_indices中
    //得到的输出格式为N * [x,y,w,h,conf(最大类别概率),class] 
    std::vector<Detection> detections{};

    //给不同类别随机生成不同颜色
    for (unsigned long i = 0; i < nms_result.size(); ++i)
    {
        int idx = nms_result[i];

        Detection result;
        result.class_id = class_ids[idx];
        result.confidence = confidences[idx];

        //生成随机颜色集合，数量等于类别数class_names
        std::random_device rd;
        //生成伪随机数生成器的种子，以提供更高质量的随机性
        std::mt19937 gen(rd());
        //生成随机数
        std::uniform_int_distribution<int> dis(100, 255);
        //随机生成一个整数，并根据分布概率函数均匀分布在一个闭区间内
        result.color = cv::Scalar(dis(gen),
                                  dis(gen),
                                  dis(gen));
        
        result.className = classes[result.class_id];
        result.box = boxes[idx];

        detections.push_back(result);
    }

    return detections;
}

//从classes.txt加载文件（不过此处并没有用到
void Inference::loadClassesFromFile()
{
    std::ifstream inputFile(classesPath);
    //打开文件filename，模式默认 ios_base::in
    if (inputFile.is_open())
    {
        std::string classLine;
        while (std::getline(inputFile, classLine))
        //getline从输入流中读取字符, 并把它们转换成字符串
            classes.push_back(classLine);
        inputFile.close();
    }
}

//加载网络和运行设备
void Inference::loadOnnxNetwork()
{
    net = cv::dnn::readNetFromONNX(modelPath);
    //读取ONNX类型模型中的网络？
    if (cudaEnabled)
    {
        std::cout << "\nRunning on CUDA" << std::endl;
        net.setPreferableBackend(cv::dnn::DNN_BACKEND_CUDA);
        net.setPreferableTarget(cv::dnn::DNN_TARGET_CUDA);
        //使用GPU作为后台计算
    }
    else
    {
        std::cout << "\nRunning on CPU" << std::endl;
        net.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
        //一般情况都是使用opencv dnn作为后台计算
        net.setPreferableTarget(cv::dnn::DNN_TARGET_CPU);
    }
}

//改变图像形状为正方形（以较长边为基准）
cv::Mat Inference::formatToSquare(const cv::Mat &source)
{
    int col = source.cols;
    int row = source.rows;
    int _max = MAX(col, row);
    cv::Mat result = cv::Mat::zeros(_max, _max, CV_8UC3);
    source.copyTo(result(cv::Rect(0, 0, col, row)));
    //把source复制到result上？
    return result;
}
