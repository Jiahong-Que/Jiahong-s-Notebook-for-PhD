CNN 教学系列 第 1 讲：什么是神经网络（MLP）

详细教学脚本，适用于视频讲解、PPT演示、或讲义内容。结构包括：引入 → 理论讲解 → 编程演示 → 互动总结。

---

# 🎓 教学脚本：第 1 讲 - 什么是神经网络（MLP）从线性分类器讲起

---

## 📌 教学目标

* 理解神经元结构和激活函数
* 理解多层感知机（MLP）的前向传播和反向传播
* 实现一个简单的 MLP 用于图像分类（MNIST）
* 为 CNN 做好基础准备

---

## ⏱️ 总时长建议：60\~75 分钟

| 模块   | 内容                   | 时间建议   |
| ---- | -------------------- | ------ |
| 引入   | 为什么需要神经网络？           | 5 min  |
| 理论讲解 | 神经元结构 + MLP 前向传播机制   | 20 min |
| 编程演示 | 用 PyTorch 实现一个两层 MLP | 25 min |
| 可视化  | 可视化权重与分类结果           | 10 min |
| 互动总结 | 回顾与小测                | 5 min  |

---

## 🧭 1. 引入：从线性分类器说起（5分钟）

🎙️ Script：

> “大家好，欢迎来到 CNN 教学系列的第一讲。今天我们从最基本的概念出发，理解神经网络模型的起点——多层感知机（MLP）。”

* 举例：逻辑回归只能画一条直线区分数据（适用于线性可分的情况）
* 现实场景复杂（如图像识别、手写字识别） → 需要非线性建模能力
* 引出：神经网络通过**激活函数 + 多层结构**，可以拟合复杂边界

---

## 🧠 2. 理论讲解（20分钟）

### ✳️ 神经元结构（单个神经元）

🎙️ Script：

> “神经元就是数学表达式：`y = f(w · x + b)`，其中 f 是非线性激活函数。”

* 公式展示：

  $$
  z = \sum_{i=1}^{n} w_i x_i + b,\quad y = \sigma(z)
  $$

* 激活函数介绍：

  * ReLU: $\text{ReLU}(x) = \max(0, x)$
  * Sigmoid: $\sigma(x) = \frac{1}{1 + e^{-x}}$
  * 为什么需要非线性？

---

### ✳️ 多层感知机结构（MLP）

🎙️ Script：

> “多层感知机通过堆叠多个神经元层，模拟复杂的映射关系。”

* 示例网络结构（用于 MNIST）：

  * 输入层：784（28×28 图像）
  * 隐藏层：128 神经元 + ReLU
  * 输出层：10 类 + Softmax

* 前向传播流程图 + 数学公式

---

### ✳️ 损失函数与反向传播

🎙️ Script：

> “神经网络通过反向传播算法不断调整参数，以最小化预测误差。”

* 使用交叉熵损失：

  $$
  \mathcal{L} = -\sum_{i} y_i \log(\hat{y}_i)
  $$
* 简述链式法则计算梯度

---

## 💻 3. 编程演示（25分钟）

🎙️ Script：

> “接下来我们动手实现一个两层的 MLP，用来识别 MNIST 手写数字。”

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# 1. 数据加载
transform = transforms.ToTensor()
train_set = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_set, batch_size=64, shuffle=True)

# 2. 定义 MLP 网络
class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(-1, 28*28)  # Flatten
        x = F.relu(self.fc1(x))
        return self.fc2(x)

model = MLP()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# 3. 训练过程
for epoch in range(1):
    for batch in train_loader:
        x, y = batch
        pred = model(x)
        loss = criterion(pred, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f"Epoch complete: Loss={loss.item():.4f}")
```

---

## 🖼️ 4. 可视化权重和预测效果（10分钟）

🎙️ Script：

> “我们可以看看隐藏层权重的可视化，它反映了模型是如何提取图像中的特征的。”

* 展示第一层 `fc1.weight` reshape 后的图像（28×28）
* 展示模型对某张图像的预测概率（用 bar chart）

---

## 🎯 5. 总结与小测（5分钟）

* 🤔 思考题：

  1. 如果没有激活函数，MLP 还能拟合复杂函数吗？
  2. 为什么使用交叉熵损失函数而不是 MSE？
  3. 隐藏层越多越好吗？

* 📌 总结：

  * MLP 是最基础的神经网络结构
  * 可以处理图像分类任务，但缺乏空间感知能力
  * CNN 在结构上对图像更友好——这将是我们下一讲的主题

---

## 📦 下一讲预告

> “下一讲我们将深入图像的世界，讲解什么是卷积，为什么卷积神经网络是图像领域的利器。”

---

如果你打算配套做视频或讲义，我还可以为这一讲：

* 提供 PPT 模板（含图示）
* 生成代码注释版本 / Jupyter Notebook
* 帮你写中英文字幕脚本或视频文案

是否需要我继续？是否现在就生成 PPT 和 Notebook？
