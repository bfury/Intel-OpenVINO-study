1、将“FPS-Counter”添加到练习1的面部检测示例中，以测量此工作负载在计算机上的性能（FPS）。

2、对单个视频输入的人脸检测模型的性能进行基准测试。

确保将MODEL-PATH设置到模型目录中。

eg: export lab_dir=~/

eg: export MODELS_PATH=~/??/??/models

本使用benchmark App来评估通道性能

**benchmark.sh**
第64行是正在运行的流水线，可以看到，这里有一个检测模型，然后使用gvafpscounter打印FPS。source元素是视频输入文件，VIDEO_PROCESSING命令取决于本实验是在英特尔集成显卡上运行，还是在CPU上运行。第70行指定了“通道数”，该脚本将反复复制GSTREAMER流水线，以得到一个长命令来模拟多个通道同时运行的情况。

运行脚本可参考命令bash benchmark.sh road.mp4 CPU CPU 1来检测通道性能，4个输入变量分别是输入视频、解码设备、推理设备、通道数。这里解码步骤在CPU上运行，并且推理阶段也在CPU上运行，只运行一个输入视频。

这个工具十分友好，可帮助你构建自己的流水线系统或仅仅是使用你的输入视频、模型对应用进行模拟，并评估系统可以服务的通道数量。你可以发挥你的创意来使用这个评估性能的小工具，可以挑选一个最喜欢的模型，并探索可以运用该模型构建一个什么样的AI程序。

执行命令vi face_detection_and_classification.sh查看并修改面部检测和分类示例代码。


可以在这里看到使用的4个模型。

步骤1
使用gvafpscounter ! fakesink替换gvawatermark ! videoconvert，使用fakesink不对生成的视频进行任何操作，具体如下。


步骤2
执行命令bash face_detection_and_classification.sh road.mp4在road.mp4视频上运行修改好的代码。




由于结果数据会持续打印，可使用Ctrl+C终止打印，可以看到，对于一个视频流，实现了每秒约10帧以上的速率。

步骤3
执行命令vi benchmark.sh查看benchmark App脚本文件。



步骤4
执行命令bash benchmark.sh road.mp4 CPU CPU 1运行脚本来检测通道性能。


这里可以看到实际运行的流水线。


可实现大约每秒10帧的速率。

步骤5
复制并运行这个流水线，该命令可以看到输入视频为road.mp4，解码并转换，gvadetect是面部检测模型。
 gst-launch-1.0 -v filesrc location=road.mp4 ! decodebin ! videoscale ! video/x-raw ! gvadetect model-instance-id=inf0 model=/root/51openlab/07/exercise-3/models/face-detection-adas-0001/FP32/face-detection-adas-0001.xml device=CPU pre-process-backend=ie ! queue ! gvafpscounter ! fakesink




步骤6
执行命令bash benchmark.sh road.mp4 CPU CPU 3运行3个通道。


在结果的开头部分，可以在此处看到实际使用的GSTREAMER流水线，filesrc location=road.mp4 ! decodebin ! videoscale ! video/x-raw ! gvadetect model-instance-id=inf0 model=/models/face-detection-adas-0001/FP32/face-detection-adas-0001.xml device=CPU pre-process-backend=ie ! queue ! gvafpscounter ! fakesink这部分是视频输入，

filesrc location=road.mp4 ! decodebin ! videoscale ! video/x-raw ! gvadetect model-instance-id=inf0 model=/models/face-detection-adas-0001/FP32/face-detection-adas-0001.xml device=CPU pre-process-backend=ie ! queue ! gvafpscounter ! fakesink这部分是第二个通道，

filesrc location=road.mp4 ! decodebin ! videoscale ! video/x-raw ! gvadetect model-instance-id=inf0 model=/root/51openlab/07/exercise-3/models/face-detection-adas-0001/FP32/face-detection-adas-0001.xml device=CPU pre-process-backend=ie ! queue ! gvafpscounter ! fakesink这部分是第三个通道。


FPS总计约为10，即3个通道中每个约为3FPS。

本项目通过模拟完整的视频分析流水线，在早期阶段检查应用的准确性和性能。这样的模拟还可以帮助你选择正确的系统，提前了解最终产品的性能，实验介绍了DL-Streamer及其如何用几行代码来模拟完整的视频分析流水线。