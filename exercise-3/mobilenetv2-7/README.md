1、学习模型优化器的输入参数。

2、使用模型优化器将mobilenet ONNX模型转换为IR文件。
验证转换的IR文件分类推理结果。

在yaml文件中，可以看到模型优化器的所有参数。

执行如下命令，使用模型优化器转换模型，输入模型参数为mobilenetv2-7.onnx，输入的均值和缩放值均为yaml文件中的值，同时将输入通道从rgb反转为bgr，运行并生成IR文件如红框中所示。
# mo.py --input_model mobilenetv2-7.onnx --mean_values=data[123.675,116.28,103.53] --scale_values=data[58.624,57.12,57.375] --reverse_input_channels --output_dir $lab_dir