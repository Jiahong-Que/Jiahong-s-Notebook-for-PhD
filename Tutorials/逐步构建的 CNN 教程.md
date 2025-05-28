一个逐步构建的 CNN 教程，不仅能加深你自己的理解，也对初学者非常有帮助。

设计一个**逐步讲解的 CNN 教程 roadmap**，每个阶段从最基础的模型和概念讲起，逐步引入复杂结构，并配合动手实现。

---

## 🧭 CNN 教程讲解 Roadmap（共 6 讲）

### ✅ 总目标：从零实现并理解 CNN，掌握图像分类的完整流程

---

### 📘 第 1 讲：什么是神经网络（MLP）——从线性分类器讲起

**目标**：理解神经元、激活函数、前向传播、损失函数和反向传播

* 简单的二分类逻辑回归模型
* 手动实现一个两层的 MLP 网络处理 MNIST 数据（784 ➝ 128 ➝ 10）
* 用图像展示权重和决策边界

> 📌 实践建议：手写一个简单的 MLP（用 numpy / PyTorch）

---

### 📘 第 2 讲：图像数据结构与卷积操作

**目标**：掌握图像的张量结构，理解什么是卷积、卷积核、stride、padding

* 图像 = Tensor(C, H, W)，以 MNIST 和 CIFAR10 举例
* 卷积 vs 矩阵乘法（动手演示）
* 代码演示 `nn.Conv2d` 的输入输出尺寸变化

> 📌 动手练习：写一个可视化卷积操作的小 demo（比如用 matplotlib 动图展示 kernel 滑动）

---

### 📘 第 3 讲：构建第一个 CNN（从零开始的 LeNet-5）

**目标**：实现经典 LeNet-5，并在 MNIST 上进行训练与测试

* Conv ➝ ReLU ➝ Pool ➝ Conv ➝ ReLU ➝ Pool ➝ FC ➝ Softmax
* 解释每一层的作用，特别是参数数量和输出尺寸的变化
* 可视化 feature maps、权重

> 📌 实践任务：实现 LeNet，比较训练准确率、损失变化，展示 feature map（中间层输出）

---

### 📘 第 4 讲：现代 CNN 模型结构（VGG / BatchNorm / Dropout）

**目标**：引入现代改进：小卷积核堆叠、正则化方法、网络深度管理

* VGG block（3x3卷积+ReLU+Pooling 的重复堆叠）
* Batch Normalization 和 Dropout 的作用（训练更快更稳）
* 构建简化版 VGG，训练 CIFAR10 数据

> 📌 实践任务：训练一个简化版 VGGNet 模型（最多 5 层）

---

### 📘 第 5 讲：模型瓶颈与突破：残差网络 ResNet

**目标**：理解深层 CNN 的退化问题，引入 ResNet 的残差连接

* 什么是梯度消失，为什么深层模型难训练
* Residual Block 的思想（identity shortcut connection）
* 搭建一个 ResNet-18 的精简版，实战 CIFAR10

> 📌 实践任务：实现 3-block 的 ResNet 并分析与 VGG 的对比

---

### 📘 第 6 讲：训练技巧 + 模型评估 + 可视化

**目标**：让你的 CNN 模型更鲁棒，更可解释，更可视化

* 学习率调整、数据增强（torchvision.transforms）、权重初始化
* confusion matrix，precision/recall，Grad-CAM（可视化模型关注区域）
* TensorBoard 简单介绍

> 📌 实践任务：用训练好的模型在测试集中预测 5 张图片，并用 Grad-CAM 高亮模型关注区域

---

## 🧰 工具建议

* 使用 **PyTorch** 框架实现（清晰直观）
* 数据集建议：

  * MNIST（手写数字）
  * CIFAR10（彩色图像）
* 可视化：

  * matplotlib（feature map）
  * seaborn（混淆矩阵）
  * torchsummary / torchinfo（模型结构概览）

---

## 🔁 学习模式建议

| 模块   | 内容                      | 时间建议       |
| ---- | ----------------------- | ---------- |
| 理论讲解 | 用图 + 示例 + 动画，讲清楚结构和原理   | 每讲15\~20分钟 |
| 编码演示 | 手把手训练模型，边讲边写            | 每讲30\~60分钟 |
| 小练习  | 给出关键任务（比如可视化、写一个 block） | 每讲1个练习     |
| 小测试  | 提问或思考题，回顾概念             | 每讲5道题      |

---

Next:

* **写每一讲的完整 script（中英双语）**
* **生成演示代码**
* **制作每讲的 PPT 或 Jupyter Notebook 教程**

