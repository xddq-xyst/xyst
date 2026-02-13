import itertools
import collections
import time
from tqdm import tqdm
import numpy as np

class PolyominoSolver:
    def __init__(self, layout_str):
        """
        layout_str: ASCII 地图
        '.' = 有效空位 (0)
        '#' = 墙壁/无效 (-1)
        """
        self.grid, self.rows, self.cols, self.valid_area = self._parse_layout(layout_str)
        self.grid_backup = self.grid.copy()
        self._init_library()
        self.solution_found = False

    def _parse_layout(self, layout_str):
        lines = [line.strip() for line in layout_str.strip().split('\n')]
        rows = len(lines)
        cols = max(len(line) for line in lines) if lines else 0

        # -1: 墙壁, 0: 空位
        grid = -np.ones((rows, cols))
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                if char == '.':
                    grid[r, c] = 0

        valid_count = (grid == 0).sum()

        return grid, rows, cols, valid_count

    def _init_library(self):
        """初始化标准形状库 (3格, 4格, 5格)"""
        lib = {}

        # 1格
        lib['S'] = [(0, 0)]

        # 2格
        lib['B'] = [(0, 0), (0, 1)]

        # --- 3格 Trominoes ---
        lib['T3_I'] = [(0, 0), (0, 1), (0, 2)]
        lib['T3_L'] = [(0, 0), (1, 0), (0, 1)]

        # --- 4格 Tetrominoes ---
        lib['T4_O'] = [(0, 0), (0, 1), (1, 0), (1, 1)]
        lib['T4_I'] = [(0, 1), (0, 2), (0, 3), (0, 4)]
        lib['T4_T'] = [(0, 0), (0, 1), (0, 2), (1, 1)]
        lib['T4_J'] = [(0, 0), (0, 1), (0, 2), (1, 2)]
        lib['T4_Z'] = [(0, 0), (0, 1), (1, 1), (1, 2)]

        # --- 5格 Pentominoes ---
        lib['P5_F'] = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
        lib['P5_I'] = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
        lib['P5_T'] = [(1, 0), (1, 1), (1, 2), (0, 2), (2, 2)]
        lib['P5_X'] = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]
        lib['P5_Z'] = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)]

        self.library = lib

        meta = {}
        meta['S'] = {'num': 1}
        meta['B'] = {'num': 2}
        meta['T3_I'] = {'num': 3}
        meta['T3_L'] = {'num': 3}
        meta['T4_O'] = {'num': 4}
        meta['T4_I'] = {'num': 4}
        meta['T4_T'] = {'num': 4}
        meta['T4_J'] = {'num': 4}
        meta['T4_Z'] = {'num': 4}
        meta['P5_F'] = {'num': 5}
        meta['P5_I'] = {'num': 5}
        meta['P5_T'] = {'num': 5}
        meta['P5_X'] = {'num': 5}
        meta['P5_Z'] = {'num': 5}
        self.meta = meta

        return

    def _get_unique_rotations(self, coords, rotations=[0, 1, 2, 3]):
        """预计算旋转并去重"""
        variations = set()
        current = coords
        for r in range(4):
            # 归一化：移到左上角
            min_r = min(p[0] for p in current)
            min_c = min(p[1] for p in current)
            normalized = tuple(sorted((p[0] - min_r, p[1] - min_c) for p in current))

            if r in rotations:
                variations.add(normalized)

            # 旋转
            current = [(p[1], -p[0]) for p in current]

        return list(variations)

    def _parse_input(self, pieces_list):
        if type(pieces_list) != dict:
            piece_counts = collections.Counter(pieces_list)
        else:  # dict
            piece_counts = pieces_list

        return piece_counts

    def solve(self, pieces_input, verbose=True):
        start_time = time.time()
        self.solution_found = False

        # 1. 统计物体数量
        piece_counts = self._parse_input(pieces_input)

        # 2. 预生成旋转缓存
        self.shapes_cache = {}
        total_piece_area = 0
        for name, count in piece_counts.items():
            coords = self.library[name]
            self.shapes_cache[name] = self._get_unique_rotations(coords, rotations=[0, 1, 2, 3])
            total_piece_area += self.meta[name]['num'] * count

        if verbose:
            print(f"有效面积: {self.valid_area}, 物体总面积: {total_piece_area}")

        if total_piece_area > self.valid_area:
            if verbose:
                print("有效面积不足")
            return False
        elif total_piece_area < self.valid_area:
            # 用单格填补
            name = 'S'
            coords = self.library[name]
            self.shapes_cache[name] = self._get_unique_rotations(coords, rotations=[0])
            piece_counts['S'] += self.valid_area - total_piece_area

        # 3. 开始回溯
        if self._backtrack(piece_counts, 1):
            if verbose:
                print(f"\n耗时: {time.time() - start_time:.4f} 秒")
                self.print_grid()
            return True
        else:
            if verbose:
                print(f"无解 (耗时 {time.time() - start_time:.4f} 秒)")
            return False

    def _find_first_empty(self):
        """
        找到第一个 0 (有效空位) 返回
        """
        indices = np.argwhere(self.grid == 0)
        if len(indices) > 0:
            first_index = indices[0]
            return first_index
        else:
            return None

    def _backtrack(self, piece_counts, next_piece_id):
        # 找到第一个需要被填补的空位
        empty_pos = self._find_first_empty()

        # 如果没有空位了，说明所有有效格子都填满了
        if empty_pos is None:
            return True

        r, c = empty_pos

        # 获取所有剩余可用的形状
        available_shapes = [k for k, v in piece_counts.items() if v > 0]

        # 启发式排序：尝试先放复杂的形状
        available_shapes.sort(key=lambda k: self.meta[k]['num'], reverse=True)

        for shape_name in available_shapes:
            piece_counts[shape_name] -= 1

            for shape_coords in self.shapes_cache[shape_name]:
                # 尝试将该形状放置，并覆盖住 (r,c) 这个点
                # 注意：这里我们遍历 shape_coords 中的每一个点作为锚点
                # 因为 (r,c) 可能是形状的中心，也可能是形状的边缘。
                # 但为了利用 find_first_empty 的特性（(r,c)是当前最左上角的空位），
                # 我们只需要让形状的“第一个点(左上角)”对准 (r,c) 即可覆盖它吗？
                #
                # 是的！因为 shape_coords 已经归一化并排序了，shape_coords[0] 必定是该形状最左上角的点。
                # 如果把 shape_coords[0] 放在 (r,c)，那么形状的其他部分都在 (r,c) 的右边或下边。
                # 既然 (r,c) 是当前全图最左上的空位，那么不可能有形状能“从左边或上边”伸过来盖住它。
                # 所以，我们只需要尝试将形状的 (0,0) 锚定在 (r,c) 这一种情况即可！
                # 这极大地减少了尝试次数。

                if self._can_place(shape_coords, r, c):
                    self._place(shape_coords, r, c, next_piece_id)

                    if self._backtrack(piece_counts, next_piece_id + 1):
                        return True

                    self._place(shape_coords, r, c, 0)  # 回溯

            piece_counts[shape_name] += 1

        return False

    def _can_place(self, shape_coords, r, c):
        """检查能否以 (r,c) 为左上角放置形状"""
        for dr, dc in shape_coords:
            nr, nc = r + dr, c + dc
            # 1. 越界检查
            if not (0 <= nr < self.rows and 0 <= nc < self.cols):
                return False
            # 2. 碰撞检查：只能放在 0 的位置
            # 如果是 -1 (墙) -> != 0 -> 返回 False (正确)
            # 如果是 > 0 (已有物体) -> != 0 -> 返回 False (正确)
            if self.grid[nr, nc] != 0:
                return False
        return True

    def _place(self, shape_coords, r, c, val):
        for dr, dc in shape_coords:
            self.grid[r + dr, c + dc] = val

    def print_grid(self):
        chars = ".ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"
        print()
        for row in self.grid:
            line_str = ""
            for cell in row:
                cell = int(cell)
                if cell == -1:
                    line_str += "█"
                elif cell == 0:
                    line_str += "."
                else:
                    idx = (cell - 1) % (len(chars) - 1)
                    char = chars[idx + 1]
                    line_str += f"{char}"
            print(line_str)
        print()

    def reset(self, backup=False):
        self.grid[self.grid != -1] = 0
        self.solution_found = False
        if backup:
            self.grid_backup[self.grid_backup != -1] = 0

    def update_grid(self, coords, use_backup=False, update_backup=False):
        if use_backup:
            self.grid = self.grid_backup.copy()
        else:
            for r, c in coords:
                self.grid[r, c] = 0

        if update_backup:
            self.grid_backup = self.grid.copy()

        self.rows, self.cols = self.grid.shape
        self.valid_area = (self.grid == 0).sum()

    def metrics(self, n3=True, n4=True, n5=False,
                n3_sub=True, n4_sub=True, n5_sub=False):
        # 可容纳多少种3格/4格/5格的排列作为衡量标准（比例）
        metric = {
            'n3': 0,
            'n4': 0,
            'n5': 0,
            'n3_sub': 0,
            'n4_sub': 0,
            'n5_sub': 0
        }

        self.reset()
        if n3:
            num3 = self.valid_area // 3
            pieces3 = [k for k in self.meta.keys() if self.meta[k]['num'] == 3]
            comb = list(itertools.combinations_with_replacement(pieces3, num3))
            metric_n3 = 0
            # for item in tqdm(comb):
            for item in comb:
                if self.solve(item, verbose=False):
                    metric_n3 += 1

                self.reset()

            metric['n3'] = metric_n3 / len(comb)

        self.reset()
        if n3_sub:
            num3 = self.valid_area // 3
            pieces3 = [k for k in self.meta.keys() if self.meta[k]['num'] == 3]
            comb = list(itertools.combinations_with_replacement(pieces3, num3 - 1))
            metric_n3_sub = 0
            # for item in tqdm(comb):
            for item in comb:
                if self.solve(item, verbose=False):
                    metric_n3_sub += 1

                self.reset()

            metric['n3_sub'] = metric_n3_sub / len(comb)

        self.reset()
        if n4:
            num4 = self.valid_area // 4
            pieces4 = [k for k in self.meta.keys() if self.meta[k]['num'] == 4]
            comb = list(itertools.combinations_with_replacement(pieces4, num4))
            metric_n4 = 0
            # for item in tqdm(comb):
            for item in comb:
                if self.solve(item, verbose=False):
                    metric_n4 += 1

                self.reset()

            metric['n4'] = metric_n4 / len(comb)

        self.reset()
        if n4_sub:
            num4 = self.valid_area // 3
            pieces4 = [k for k in self.meta.keys() if self.meta[k]['num'] == 3]
            comb = list(itertools.combinations_with_replacement(pieces4, num4 - 1))
            metric_n4_sub = 0
            # for item in tqdm(comb):
            for item in comb:
                if self.solve(item, verbose=False):
                    metric_n4_sub += 1

                self.reset()

            metric['n4_sub'] = metric_n4_sub / len(comb)

        self.reset()
        if n5:
            num5 = self.valid_area // 5
            pieces5 = [k for k in self.meta.keys() if self.meta[k]['num'] == 5]
            comb = list(itertools.combinations_with_replacement(pieces5, num5))
            metric_n5 = 0
            for item in tqdm(comb):
                if self.solve(item, verbose=False):
                    metric_n5 += 1

                self.reset()

            metric['n5'] = metric_n5 / len(comb)

        self.reset()
        if n5_sub:
            num5 = self.valid_area // 3
            pieces5 = [k for k in self.meta.keys() if self.meta[k]['num'] == 3]
            comb = list(itertools.combinations_with_replacement(pieces5, num5 - 1))
            metric_n5_sub = 0
            for item in tqdm(comb):
                if self.solve(item, verbose=False):
                    metric_n5_sub += 1

                self.reset()

            metric['n5_sub'] = metric_n5_sub / len(comb)

        return metric

    def frontier(self):
        zero_mask = (self.grid == 0)
        neighbor_mask = np.zeros_like(zero_mask, dtype=bool)
        neighbor_mask[1:, :] |= zero_mask[:-1, :]  # 下邻居
        neighbor_mask[:-1, :] |= zero_mask[1:, :]  # 上邻居
        neighbor_mask[:, 1:] |= zero_mask[:, :-1]  # 右邻居
        neighbor_mask[:, :-1] |= zero_mask[:, 1:]  # 左邻居
        neighbor_mask &= ~zero_mask
        coords = np.argwhere(neighbor_mask)
        return coords


# ================= 测试 =================

if __name__ == "__main__":
    layout = '''
        ##########
        ##########
        ##########
        ###......#
        ###.....##
        ###.....##
        ###.....##
        ##########
        ##########
        ##########
        ##########
        '''
    pieces_input = {
        # 单格
        'S': 0,
        # 2格
        'B': 1,
        # 3格
        'T3_I': 4,
        'T3_L': 2,
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

    solver = PolyominoSolver(layout)
    solver.solve(pieces_input)

