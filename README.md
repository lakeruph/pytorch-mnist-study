# PyTorch MNIST 学习与推理验证项目

> 基于 [PyTorch 官方 examples/mnist](https://github.com/pytorch/examples/tree/main/mnist) 的学习实践，重点是理解训练流程、保存与恢复权重，以及独立验证推理结果。本项目不是原创网络结构或新的分类算法。

## 1. 项目简介

本项目以 MNIST 手写数字分类为例，完成了 PyTorch 模型训练、测试、权重保存与加载、单样本预测及完整测试集评估，并在控制其他参数的情况下对比了不同学习率的测试表现。

已验证的主要结果：使用默认学习率 `1.0`、训练 `3` 个 Epoch（轮次）后，测试集 10,000 张图像中正确分类 9,902 张，准确率为 **99.02%**；将保存的模型权重加载到新建网络后，独立评估复现了同样的准确率。

## 2. 实验环境

以下是本次实际运行时记录的环境，而非要求所有使用者完全一致：

| 项目       | 记录                                  |
| -------- | ----------------------------------- |
| 操作系统     | Windows（PowerShell / VS Code）       |
| Python   | 3.10.21                             |
| PyTorch  | 2.14.0+cu126（本地环境报告值）               |
| CUDA 可用性 | `torch.cuda.is_available() == True` |
| 数据集      | MNIST（训练集 60,000 张；测试集 10,000 张）    |

> 注意：CUDA 可用不等于已单独验证本次训练的实际执行设备。运行时需安装兼容版本的 `torch` 和 `torchvision`。

## 3. 项目相关目录

以下仅列出本次学习涉及的文件；基于官方 `pytorch/examples` 的本地仓库可能还包含其他示例。

```text
pytorch-mnist-study/
├── README.md                        # 本项目说明文档
├── experiments/
│   └── lr_comparison.md             # 学习率对比实验记录
└── mnist/
    ├── main.py                  # 官方 MNIST 训练与测试示例
    ├── verify_checkpoint.py     # 独立编写的模型恢复与评估脚本
    └── README.md                # 保留原有说明文件
```

训练产生的 `mnist_cnn.pt` 和备份 `mnist_cnn_baseline_e3.pt` 属于本地模型权重文件，**不要求上传到 GitHub**；可通过以下步骤重新生成。

## 4. 运行方法

打开 PowerShell，进入 MNIST 示例目录（以下命令假设当前位于仓库根目录）：

```powershell
cd .\mnist
```

### 4.1 基准训练：学习率 1.0

```powershell
python main.py --epochs 3 --seed 1 --lr 1.0 --save-model
```

本次实验中，`batch_size=64`、学习率衰减系数 `gamma=0.7` 使用脚本默认值。程序完成三轮训练与测试后，会在当前工作目录生成 `mnist_cnn.pt`。

若希望保留这次基准模型供后续独立评估使用，请在重新训练前备份：

```powershell
Copy-Item .\mnist_cnn.pt .\mnist_cnn_baseline_e3.pt
```

### 4.2 加载权重并独立评估

```powershell
python verify_checkpoint.py
```

该脚本从当前目录读取 `mnist_cnn_baseline_e3.pt`，使用 CPU 恢复网络权重，并对 MNIST 测试集进行逐批预测。请从 `examples/mnist` 目录执行，以便相对路径正常解析。

### 4.3 学习率对比训练：学习率 0.5

```powershell
python main.py --epochs 3 --seed 1 --lr 0.5
```

此命令不添加 `--save-model`，避免覆盖基准模型权重。

## 5. 实验结果

各指标均来自实际训练日志；Accuracy 按正确预测数 / 10,000 计算，未采用终端显示的整数百分比。

| Epoch | LR=1.0 测试 Loss | LR=1.0 Accuracy | LR=0.5 测试 Loss | LR=0.5 Accuracy |
| -----:| --------------:| ---------------:| --------------:| ---------------:|
| 1     | 0.0583         | 98.16%          | 0.0495         | 98.27%          |
| 2     | 0.0368         | 98.73%          | 0.0358         | 98.71%          |
| 3     | 0.0323         | **99.02%**      | 0.0321         | 98.83%          |

基准模型独立加载后的完整测试集结果：

```text
Total samples:10000
Correct predictions:9902
Accuracy:99.02%
```

**观察：** `LR=0.5` 在第 1 轮的测试准确率略高，但第 3 轮低于 `LR=1.0`；同时，其测试平均 Loss 略低。测试损失与分类准确率不必同步变化。当前只是两组单次实验，不能据此断言某个学习率在所有随机种子或训练条件下都更优。

更完整的记录见 [学习率对比实验](./experiments/lr_comparison.md)。

## 6. 当前范围与后续方向

已验证：三轮训练、模型权重保存和重新加载、单张真实测试图像预测、完整测试集评估、学习率对比。

后续可在该基础上开展 ONNX（Open Neural Network Exchange，开放神经网络交换格式）导出，以及 ONNX Runtime 的 Python / C++ 推理正确性对比。本仓库当前**不宣称已完成** ONNX Runtime 部署或性能 Benchmark。

## 7. 来源与许可

训练脚本与网络结构来自 [PyTorch Examples](https://github.com/pytorch/examples)。该上游仓库采用 [BSD 3-Clause License](https://github.com/pytorch/examples/blob/main/LICENSE)。如再分发上游源代码，请保留原项目的版权和许可声明，并明确区分个人编写的验证脚本、实验结果与上游代码。

本项目仅使用公开 MNIST 数据及许可允许的代码，不应添加任何保密科研材料、访问令牌或私人数据。
