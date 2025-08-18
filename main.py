from ykzf_utils import *

items = [
    {'name':'武器', 'value':3325, 'type':0, 'rate':None, 'dir': None},
    {'name':'头盔', 'value':3019,  'type':0, 'rate':None, 'dir': None},
    {'name':'盔甲', 'value':3487,  'type':0, 'rate':None, 'dir': None},
    {'name':'背饰', 'value':3158,  'type':0, 'rate':None, 'dir': None},
    {'name':'护腕', 'value':3989,  'type':0, 'rate':None, 'dir': None},
    {'name':'护腿', 'value':3988,  'type':0, 'rate':None, 'dir': None},
    {'name':'星盘', 'value':1156,  'type':1, 'rate':0.15, 'dir': 'up'},
    {'name':'神识', 'value':1584, 'type':2, 'rate':0.075, 'dir': 'left'},
    {'name':'核心', 'value':1144,  'type':3, 'rate':0.083, 'dir': 'anti'},
]

basic_score = 1337
bonus1 = 0.05
bonus2 = 0.128

result = maximize_grid(items)
print("Best Score:", result['best_score'])
print("Total Score:", (result['best_score'] + basic_score) * (1 + bonus1) * (1 + bonus2))
for r in result['grid']:
    print([name for name in r])
