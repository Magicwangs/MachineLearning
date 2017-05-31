## logistic 回归

## 过程
- 找一个合适的预测函数——h函数  
  该函数就是我们需要找的分类函数，它用来预测输入数据的判断结果。这个过程时非常关键的，需要对数据有一定的了解或分析，知道或者猜测预测函数的“大概”形式，比如是线性函数还是非线性函数。  
  如 w0+w1*X1....+Wi*Xi的形式  

- 构造一个Cost函数（损失函数）  
  该函数表示预测的输出（h）与训练数据类别（y）之间的偏差，可以是二者之间的差（h-y）或者是其他的形式。综合考虑所有训练数据的“损失”，将Cost求和或者求平均，记为J(θ)函数，表示所有训练数据预测值与实际类别的偏差。   

- 显然，J(θ)函数的值越小表示预测函数（h函数）越准确，所以这一步需要做的是找到J(θ)函数的最小值。  
  找函数的最小值有不同的方法，Logistic Regression实现时有的是梯度下降（Gradient Descent）有的是梯度上升（Gradient Ascent）    



## 参考
- [Blog](http://blog.csdn.net/dongtingzhizi/article/details/15962797)  
- [Andrew Ng](http://open.163.com/special/opencourse/machinelearning.html)  
