# 意见模型

基本的意见传播模型，见
Netlogo vs. Julia: Evaluating Different Options for the Simulation of Opinion Dynamics

见书：duffy_2020_DigitalHuman

## 基本算法

如果AB观点接近，则更接近；
如果允许backfire，AB观点较远，则更远；

1. 每个个人的观点，服从0到1的随机分布
2. 2个人比较观点；
3. A和B比较观点
   1. 如果差异小于epsilon，则A的观点向B移动一半距离。
   2. 如果允许backfire
       1. 如果A的观点较小，则A减去AB之差的一半
       2. 如果A的观点较大，则A加上AB之差的一半
       3. A的观点在[0,1]中间


   
