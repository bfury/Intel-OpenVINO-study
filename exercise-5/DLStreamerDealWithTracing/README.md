**确保将MODEL-PATH设置到模型目录中。**

eg: export lab_dir=~/

eg: export MODELS_PATH=~/??/??/models

1、学习使用DL-Streamer追踪图像的方法。

2、运行车辆追踪处理流水线。

构建流水线系统非常容易，即使是对于在跟踪应用中需要跨帧算法的实施也非常简单，跟踪是一项非常重要的功能。如果一个橙子，并且整个图像向左侧移动，那么这可能是相同的一个橙子，通过比较图片，可以知道，几帧后这可能就是相同的橙子。

如果同一对象在屏幕上移动，可以对其进行跟踪，这意味着可以判断是同一对象在移动，没必要重新检测它，这将节省大量计算能力。既然人类一直都在这样做，那么为什么不使用计算机去做呢？下面使用DL-Streamer来事半功倍的完成这个任务。

**执行命令vi vehicle_pedestrian_tracking.sh-file查看代码。**

可以看到这里有3个模型，1个用于检测，2个用于识别。

第67行可以看到Gstreamer流水线。“source element”是视频文件，将其解码，将视频转换为正确的大小和格式。第69-74行是第一次检测，可以看到所有参数、模型、检测间隔、设备等。在第75行可以看到跟踪，这个流水线阶段将跟踪前一阶段检测到的所有对象。第77和82行是另外两个模型，人员分类模型和车辆分类模型，然后使用GVAWaterMark将所有结果渲染到视频中，并输出视频文件。

**执行命令vi vehicle_pedestrian_tracking-file.sh**

编辑代码，根据需要对该文件进行更改，以构建自己的流水线，还可以添加自己的模型，或实施其他操作。比如，我们可以在这里将删除车辆属性分类。