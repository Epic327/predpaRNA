# PredPaRNA  System

## Introduction

该项目利用深度学习中的预训练模型对RNA序列进行编码，然后将其输入进深度学习模型中训练并自我学习内部的特征，最后根据模型预测的概率值来判断RNA序列的类别。选择性能最优的模型部署上线，用户通过在网站页面进行简易的操作就能在线预测RNA序列，极大的方便了生物信息学者的研究以及科研效率的提高。



## Environment

- bert4keras==0.10.8  

- keras==2.3.1

- tensorflow-gpu==2.3.0

	



## Backend

选择轻量级的flask框架进行开发，用户在浏览器向服务端发送http请求，Web服务器则将所有请求交付给Flask的应用实例，然后Flask实例中的路由模块将请求分发至相应的API并找到具体操作逻辑的视图函数。当视图函数处理完当前请求后，会将结果传入到模板并动态渲染服务端响应的数据，最终由Flask实例将其返回给前端浏览器进行展示。



## Usage

```
1.模型构建 (. 的意思是项目根目录里的Dockfile)
docker build -t image_name:v1 . 

2.运行容器
docker run -p 8080:80 -d --name parna_model pred_parna:v1
```



## Model

将1维的CNN与BiLSTM网络组合而成CNN-BiLSTM模型，该模型既拥有CNN捕获序列局部特征的能力，又拥有BiLSTM网络捕获序列上下文特征的能力。在项目model目录中，加入自己训练好的模型即可。

![](https://cdn.jsdelivr.net/gh/Epic327/code_study/picgomodel_cnn-bilstm.svg)


