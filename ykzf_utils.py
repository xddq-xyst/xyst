import numpy as np
from itertools import permutations
from tqdm import tqdm

idx2coord = [np.asarray([[r, c]]) for r in range(3) for c in range(3)]

# relative
dir2coord_type1 = {
    'up': np.asarray([
        [-1, 0]
    ]),
    'down': np.asarray([
        [1, 0]
    ]),
    'left': np.asarray([
        [0, -1]
    ]),
    'right': np.asarray([
        [0, 1]
    ]),
}

# relative
dir2coord_type2 = {
    'up': np.asarray([
        [-1, -1], [-1, 0], [-1, 1]
    ]),
    'down': np.asarray([
        [1, -1], [1, 0], [1, 1]
    ]),
    'left': np.asarray([
        [-1, -1], [0, -1], [1, -1]
    ]),
    'right': np.asarray([
        [-1, 1], [0, 1], [1, 1]
    ]),
}

# absolute
dir2coord_type3 = {
    'main': np.asarray([
        [0, 0], [1, 1], [2, 2]
    ]),
    'anti': np.asarray([
        [0, 2], [1, 1], [2, 0]
    ]),
}

def get_impact_coords(type_id, pos, dir):
    coord = idx2coord[pos]

    if type_id == 1:
        impact_coords = coord + dir2coord_type1[dir]
    elif type_id == 2:
        impact_coords = coord + dir2coord_type2[dir]
    elif type_id == 3:
        impact_coords = dir2coord_type3[dir]
    else:
        return None

    if (impact_coords >= 0).all() and (impact_coords <= 2).all():
        return impact_coords

    return None

def evaluate_layout(items):
    values = np.asarray([it['value'] for it in items]).reshape(3, 3)
    base_sum = values.sum()

    total_bonus = 0.0
    for pos, item in enumerate(items):
        type_id = item['type']
        rate = item['rate']
        dir = item['dir']

        impact_coords = get_impact_coords(type_id, pos, dir)
        if impact_coords is not None:
            total_bonus += values[impact_coords[:, 0], impact_coords[:, 1]].sum() * rate

    return base_sum + total_bonus

def maximize_grid(items):
    best = {'score': float('-inf'), 'perm': None}

    for perm in tqdm(permutations(items, 9)):
        score = evaluate_layout(perm)
        if score > best['score']:
            best['score'], best['perm'] = score, perm

    grid = []
    for r in range(3):
        row = []
        for c in range(3):
            pos = r * 3 + c
            it = best['perm'][pos]
            row.append(it['name'])
        grid.append(row)

    return {'best_score': best['score'], 'grid': grid}
