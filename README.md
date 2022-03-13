# Mesa使用NetLogo作为绘图界面

1. 使用Mesa，创建无空间的Wealth模型
2. Wealth模型使用交互分析的脚本，有cell block
3. 使用pyNetLogo
4. Mesa版比NetLogo版慢5~6倍

## 文件结构

1. mesa_money_model.py: 主模型
2. money_model.nlogo: 用来绘图的NetLogo模型
3. NL.py: pyNetLogo的包装，提供方便的函数