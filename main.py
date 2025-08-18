from ykzf_utils import *

items = [
    {'name':'A', 'value':100, 'type':1, 'rate':0.20, 'dir': 'left'},
    {'name':'B', 'value':80,  'type':2, 'rate':0.10, 'dir': 'down'},
    {'name':'C', 'value':60,  'type':3, 'rate':0.15, 'dir': 'main'},
    {'name':'D', 'value':50,  'type':0, 'rate':None, 'dir': None},
    {'name':'E', 'value':90,  'type':0, 'rate':None, 'dir': None},
    {'name':'F', 'value':70,  'type':0, 'rate':None, 'dir': None},
    {'name':'G', 'value':40,  'type':0, 'rate':None, 'dir': None},
    {'name':'H', 'value':110, 'type':0, 'rate':None, 'dir': None},
    {'name':'I', 'value':95,  'type':0, 'rate':None, 'dir': None},
]

result = maximize_grid(items)
print("Best Score:", result['best_score'])
for r in result['grid']:
    print([name for name in r])
