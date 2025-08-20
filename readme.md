# 御傀争锋最优装备分配
作者: 织梦山11/20服 大眼松鼠

## 用法

在`main.py`中填写装备数值和类型，其他信息选填（不影响装备排列位置），然后直接运行即可

```bash
python main.py
```

## 类型说明

- type 0: 无特殊效果
- type 1: 相邻一格加成，方向取'up'/'down'/'left'/'right'
- type 2: 相邻一行/列加成，方向取'up'/'down'/'left'/'right'
- type 3: 对角线加成，方向取'main-up'/'main-down'/'anti-up'/'anti-down'
  
**note:** main-up(↖)与anti-up(↗)实现反了，实际↖填写anti-up，↗填写main-up
