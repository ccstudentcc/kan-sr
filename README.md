# KAN 符号回归实验集

这个仓库汇总了我们围绕 Kolmogorov-Arnold 网络（KAN）开展的符号回归实验结果，重点展示 KAN 在可解释建模任务中的表现。

KAN 由 Liu 等人在论文 [KAN: Kolmogorov-Arnold Networks](https://arxiv.org/abs/2404.19756) 中提出。

## 📘 学位论文

### ▶️ [Approaching symbolic regression with Kolmogorov-Arnold networks [PDF]](https://github.com/user-attachments/files/17318281/Approaching.symbolic.regression.with.Kolmogorov-Arnold.networks.pdf)

## 📙 答辩展示材料

### ▶️ [Symbolic Regression with KANs [PDF]](https://github.com/user-attachments/files/17270435/Symbolic.Regression.with.KANs.pdf)

### ▶️ [Symbolic Regression with KANs [PPTX]](https://github.com/user-attachments/files/17270436/Symbolic.Regression.with.KANs.pptx)

## 📦 仓库内容一览

## 🗂️ 文件管理规范（简要）

- 实验输出统一写入 `output/`
- 文档说明统一放 `docs/`
- Notebook 统一放 `notebooks/`
- 自动化入口统一放 `scripts/`
- 详细规范见 `spec/repository-layout.md`

### [单变量符号回归方法对比](notebooks/Comparison_of_different_methods_for_SR_univariate.ipynb)

在同一单变量任务上，对比 *KAN*、*遗传编程*、*贝叶斯方法* 和 *QLattice* 的效果。

<p align="center">
<img src="img/comparison_univariate.png" alt="" width="900rem">
</p>

### [多变量符号回归方法对比](notebooks/Comparison_of_different_methods_for_SR_multivariate.ipynb)

在同一多变量任务上，对比 *KAN*、*遗传编程*、*贝叶斯方法* 和 *QLattice* 的效果。

<p align="center">
<img src="img/comparison_multivariate.png" alt="" width="1200rem">
</p>

### [摆运动实验](notebooks/Pendulum_Motion.ipynb)

我们用手机记录了 50 cm 细绳摆动过程中的陀螺仪与加速度计数据。

实验目标是在噪声存在的条件下，让 KAN 反推出简谐运动的符号表达式。

<p align="center">
  <img src="img/gyroscope.png" alt="" width="600rem">
</p>
<p align="center">
  <img src="img/accelerometer.png" alt="" width="600rem">
</p>

### [特殊函数实验](notebooks/Special_function.ipynb)

该实验聚焦正弦积分函数：

$$Si(x) = \int_0^x \frac{\sin(t)}{t} dt$$

该函数无法写成常见初等函数的有限复合，因此属于典型的特殊函数。与多数符号回归算法相比，PyKAN 依然可以给出可用近似，但精度会受到网络深度影响。

为了保持表达式可解释性，我们有意使用较小网络，而不是单纯追求极致精度。

真实函数：

<p align="center">
<img src="img/sine_integral.png" alt="" width="600rem">
</p>

KAN 学得的表达式：

$$2.5cos(1.5sin(0.17sin(-1.8x-6.2)+3.9)-0.3)-1.4$$

<p align="center">
  <img src="img/kan_sine_integral.png" alt="" width="300rem">
</p>

### [无监督学习实验](notebooks/Unsupervised_Learning.ipynb)

该实验尝试求解一个无监督关系发现问题。数据集中共有 7 个变量，满足以下关系：

- $x_2=sin(6x_0)+e^{2x_1}$
- $x_6=4x_3+x_4+x_5$

KAN 需要仅根据变量观测值自动识别这些结构关系。

<p align="center">
  <img src="img/kan_unsupervised_1.png" alt="Image 1" width="300rem">
  <img src="img/kan_unsupervised_2.png" alt="Image 2" width="300rem">
</p>

### [EfficientKAN 激活可视化](notebooks/Plotting_Efficient_KAN.ipynb)

该笔记本提供了 EfficientKAN 网络 `.plot()` 方法的基础实现，用于模型可解释性可视化。

### [压缩查找表规模](notebooks/Reducing_the_lookup_table_size.ipynb)

这个实验利用 KAN 的回归能力，将经典多变量牛顿引力定律近似为若干单变量函数的组合，以降低查找表开销。

$$F(m_1,m_2,d)=G\cdot \frac{m1\cdot m2}{d^2}$$

<p align="center">
  <img src="img/effkan_newton.png" alt="Image 2" width="500rem">
</p>

在得到可接受的训练结果后，我们展示了查找表规模随采样数线性增长。相比经典查找表的 $\mathcal{O}(N^d)$ 增长，这一方案可显著降低存储成本。

<a name="Authors"></a>

## 👨🏻‍💻 作者

| 姓名              | 邮箱                        | GitHub                                          |
|-------------------|-----------------------------|-------------------------------------------------|
| Valerio Morelli   | s1118781@studenti.univpm.it | [MrPio](https://github.com/MrPio)               |
| Federica Paganica | s1116749@studenti.univpm.it | [Federica](https://github.com/federicapaganica) |
