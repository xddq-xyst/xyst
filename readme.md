# 仙域商途路线规划
作者: 织梦山11服 大眼松鼠

## 环境安装

```bash
git clone https://github.com/xddq-xyst/xyst.git
cd xyst

conda create -n xyst python=3.9
conda activate xyst
pip install numpy==1.23 pandas tqdm openpyxl
```

## 数据准备

我在`./data/example_data.xlsx`提供了样例数据。
对于自定义数据，请仿照此填写每一处地点每一个货物的具体价格，这可以通过共享文档号召同一分组的人共同填写。

## 用法

提前规划好当天跑船次数，根据初始条件运行`main.py`，如初始资金6800，计划跑6次：

```bash
python main.py --data_path ./data/example_data.xlsx --funds_init 6800 --num_trans 6
```

## 输出说明
输出文件`./output/6800_6.txt`提供了对于每一初始位置在初始资金6800跑6次的策略，如:
```bash
### 初始北寒界:
第1次发船: (寒烟鹿茸:38, )->仙竹林
到达后资金8814
第2次发船: (天青竹:36, 苍云仙芝:1)->破虚门
到达后资金12963，飞行舟升级，当前库存倍率4
第3次发船: (太虚星草:23, )->仙竹林
到达后资金16367
第4次发船: (天青竹:67, 菩提子:1)->破虚门
**第4次发船后因超库存建议停止加速，以下策略为刷新库存后，库存倍率4**
到达后资金24095，飞行舟升级，当前库存倍率9
第5次发船: (太虚星草:42, 寒烟鹿茸:2)->文津阁
到达后资金32639，飞行舟升级，当前库存倍率21
第6次发船: (慧心果:80, 苍云仙芝:2)->石林
到达后资金47389
```

若策略中超库存提醒次数小于等于2，则可完全按照该路线跑船，否则有两种思路：
- 减少跑船次数至3次超库存提醒前，并设置新次数重跑`main.py`
- 检查是否有超库存提醒后飞行舟立即升级情况，可在刷新库存前1分钟加速，待刷新后再出发

第二种思路仍需根据更新的初始资金和剩余计划跑船次数重跑`main.py`以获得更新的超库存提醒。

我同样在最后提供了迫不得已必须超库存的策略，需要注意的是，该策略利用了贪心简化因而并非最优，且只考虑了购买两种货物情况，请谨慎使用。

## 与贪心策略比较
```bash
python main.py --data_path ./data/example_data.xlsx --funds_init 6800 --num_trans 6 --greedy
```

```bash
### 初始北寒界:
第1次发船: (寒烟鹿茸:38, )->仙竹林
到达后资金8814
第2次发船: (天青竹:36, 苍云仙芝:1)->破虚门
到达后资金12963，飞行舟升级，当前库存倍率4
第3次发船: (太虚星草:23, )->离火境
到达后资金17839
第4次发船: (火凤羽:36, 灵璧石:2)->青莲台
到达后资金25233，飞行舟升级，当前库存倍率9
第5次发船: (五彩玄莲:95, 苍云仙芝:1)->天机阁
**第5次发船后因超库存建议停止加速，以下策略为刷新库存后，库存倍率9**
到达后资金33600，飞行舟升级，当前库存倍率21
第6次发船: (赤玄铁:52, 永夜明珠:1)->北寒界
到达后资金43971
```