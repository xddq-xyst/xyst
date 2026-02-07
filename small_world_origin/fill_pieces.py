from polyomino import PolyominoSolver

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
pieces_input = {
    # 单格
    'S': 0,
    # 2格
    'B': 3,
    # 3格
    'T3_I': 1,
    'T3_L': 1,
    # 4格
    'T4_O': 0,
    'T4_I': 0,
    'T4_T': 0,
    'T4_J': 0,
    'T4_Z': 0,
    # 5格
    'P5_F': 0,
    'P5_I': 0,
    'P5_T': 0,
    'P5_X': 0,
    'P5_Z': 0
}

Polyomino = PolyominoSolver(layout)
Polyomino.solve(pieces_input)
