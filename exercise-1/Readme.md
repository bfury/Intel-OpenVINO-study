1.第一步是获取一个可执行面部检测的深度学习模型。该模型可以检测输入图像中的面部信息。

2.然后需要定义哪个设备来运行推理，如CPU集成显卡，FPGA或其他。

3.下一步是读取图像。

4.接下来对图像进行推理准备，主要是调整其大小，以适合深度学习神经网络的输入维度。

5.然后运行推理并获得结果。

6.然后在检测到的面部上画框。

7.最后将图像保存到文件中。

confidence数值越小，可以识别出的人脸越多，但可能将别的东西识别为人脸