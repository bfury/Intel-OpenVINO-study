# Intel-OpenVINO-study
For OpenVINO Study

**有问题或者建议可以发issue一起讨论学习**

目前文件目录有点混乱，但要复习考试，后面再整理规范一下～(懒惰.jpg)

需要安装OpenVINO套件 我在实验过程中使用的是2021.4版本

部分python脚本对应老版本openVINO（2020.2）

这部分的脚本对应的新版本脚本为xx_new.py

注意：直接在Pycharm的Run configuration中无法运行

因为openvino包含的针对Intel优化的opencv没有在python的site-package中

我们在CLI中成功运行是因为source了openVINO的setup.sh将相关环境变量都配置到了【终端】

而pycharm不管是虚拟环境还是本地真实解释器都没有执行相关操作

所以如要运行建议在Terminal中运行～

eg:python3 ./exercise-1/face-detection01.py

或者参考使用中的subprocess.call方法来改善

此时注意不能通过增加os.system(/路径/setup.sh)的方式来配置环境变量到pycharm进程中

因为子进程配置了环境变量，不会影响父进程, subprocess.call不在子shell中执行～

由于将全部文件（包括图片和视频资源）都上传到仓库了，因此它很大～

如果pull过慢，可以在本地完成IR模型的生成，只下载原始模型(caffe、onnx)，视频和图片也可以使用自己本地的资源代替～

