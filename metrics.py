from polyomino import PolyominoSolver
from tqdm import tqdm

layout = '''
##########
##########
##########
##########
###....###
###....###
###....###
##########
##########
##########
##########
'''

Polyomino = PolyominoSolver(layout)

# 选用哪些指标
metric_types = {'n3': True, 'n4': True, 'n5':False,
                'n3_sub': True, 'n4_sub': True, 'n5_sub':False}

# 用当前网格能够容纳多少种不同的碎片组合作为衡量标准
print(Polyomino.metrics())

# 下一个解锁槽位
for i in range(1):
    frontier = Polyomino.frontier()
    metric_best = 0
    coord_best = None
    for coord in tqdm(frontier):
        Polyomino.update_grid([coord])
        metrics = Polyomino.metrics(**metric_types)
        metrics_sum = sum(metrics.values())
        if metrics_sum > metric_best:
            metric_best = metrics_sum
            coord_best = coord

        Polyomino.reset()
        Polyomino.update_grid(None, use_backup=True)

    Polyomino.reset()
    Polyomino.update_grid(None, use_backup=True)
    Polyomino.update_grid([coord_best], update_backup=True)
    Polyomino.print_grid()
