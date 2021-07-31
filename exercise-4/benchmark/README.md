1、了解影响性能的关键因素。

2、学习benchmark的各个参数含义。

3、使用benchmark测试异步推理和同步推理模式下两个模型的性能。

4、挑战benchmark nstream和nireq的参数的用法。

性能度量是衡量一个模型泛化能力的评价标准，其包括了准确率和错误率，是深度学习研究的关键因素，但是这不是衡量模型实现或部署的关键因素。通常，越是精确的模型就越重，需要更多的计算，因此性能会降低。所以一般通过吞吐量、延迟等几个关键因素来衡量模型的性能好坏。

吞吐量：吞吐量表示神经网络在一秒钟内可以处理的帧数。一般情况下通过FPS每秒帧数，来衡量吞吐量的大小。但很多时候，每一帧会有多于1次的推理。例如，我们需对一个图片中的2辆汽车进行分类，因此衡量吞吐量更准确的参数是“每秒推理数”。

延迟：延迟表示从数据开始分析到结果可以被读取的时间，一般以秒为单位。在实际应用中，该时间不仅可以包括推理时间，也包括例如视频处理等其它阶段的时间。

另外，有许多因素可能会影响特定设备上的神经网络的性能。其中包括神经网络本身的拓扑或架构、目标设备、模型精度。所以在进行模型操作时，需要根据实际选择合适的网络和计算设备，例如CPU、GPU或FPGA等，并选择合适的输入数据格式和权重，以提升模型性能。

在异步推理模式下，使用benchmark_app.py测试resnet-50.xml和ssd-mobilenet.xml模型的性能。首先执行如下命令，使用benchmark_app.py测试resnet-50.xml模型，输入内容为images目录下所有图片文件。

`python3 benchmark_app.py -m models/resnet-50.xml -i images/`

执行如下命令，使用benchmark_app.py测试ssd-mobilenet.xml模型。测试输入为images目录下所有图片文件。

 `python3 benchmark_app.py -m models/ssd-mobilenet.xml -i images/`

在同步推理模式下，执行如下命令，使用benchmark_app.py测试ssd-mobilenet.xml模型的性能，并与其在异步推理模式下的性能对比。测试输入为images目录下所有图片文件。

 `python3 benchmark_app.py -m models/ssd-mobilenet.xml -i images/ --api sync`

在异步推理模式下，尝试挑战benchmark-app.py输入不同的参数，测试ssd-mobilenet.xml模型的性能。

(1)执行如下命令，测试ssd-mobilenet模型在2推理请求，2 streams下的性能。

 `python3 benchmark_app.py -m models/ssd-mobilenet.xml -i images/ -nstreams 2 -nireq 2`

(2)执行如下命令，测试ssd-mobilenet模型在batch为4下的异步推理性能。

 `python3 benchmark_app.py -m models/ssd-mobilenet.xml -i images/ -b 4`

(3)执行如下命令，测试ssd-mobilenet模型在batch为4下的异步推理性能，并且将perf_counts和progress 选项设置为可见。

 `python3 benchmark_app.py -m models/ssd-mobilenet.xml -i images/ -b 4 -pc true -progress true`