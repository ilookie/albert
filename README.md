# 模型训练示例

这是一个简单的深度学习模型训练示例，展示了完整的训练流程，包括：

- 数据生成和预处理
- 模型定义
- 训练循环
- 模型评估
- 损失可视化

## 环境要求

请确保安装所有必要的依赖：

```bash
pip install -r requirements.txt
```

## 运行示例

直接运行 Python 文件即可：

```bash
python train_example.py
```

## 代码结构

- `SimpleDataset`: 自定义数据集类，用于加载训练数据
- `SimpleNet`: 简单的神经网络模型定义
- `train_model`: 模型训练函数
- `evaluate_model`: 模型评估函数
- `generate_data`: 生成示例数据的函数

## 输出

程序运行后会：
1. 打印训练过程中的损失值
2. 保存训练和测试损失的曲线图（loss_curve.png）
3. 显示最终的训练和测试损失
