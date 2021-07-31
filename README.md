# Intel-OpenVINO-study
For OpenVINO Study

注意：直接在Pycharm的Run configuration中无法运行

因为openvino包含的针对Intel优化的opencv没有在python的site-package中

我们在CLI中成功运行是因为source了openVINO的setup.sh将相关环境变量都配置到了【终端】

而pycharm不管是虚拟环境还是本地真实解释器都没有执行相关操作

所以如要运行建议在Terminal中运行～

eg:python3 ./exercise-1/face-detection01.py

或者参考使用中的subprocess.call方法来改善

此时注意不能通过增加os.system(/路径/setup.sh)的方式来配置环境变量到pycharm进程中

因为子进程配置了环境变量，不会影响父进程, subprocess.call不在子shell中执行～