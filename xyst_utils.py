import numpy as np


################## Base information #####################
locations = [
    '北寒界', '石林', '雾隐谷', '紫霄仙宫', '青莲台',
    '瑶池仙岛', '天机阁', '离火境', '悟道楼', '文津阁',
    '天剑峰', '破虚门', '仙竹林', '昆仑秘境', '青冥宫'
]
goods = [
    '灵璧石', '苍云仙芝', '菩提子', '寒烟鹿茸', '五彩玄莲',
    '天青竹', '永夜明珠', '九幽玉', '慧心果', '仙蚕丝绸',
    '火凤羽', '七须灵参', '赤玄铁', '太虚星草', '九曲仙酿'
]
base_price = np.array(
    [[100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     #
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     #
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800],
     [100, 100, 200, 200, 300, 300, 400, 400, 500, 500, 600, 600, 700, 700, 800]]
)
base_inventory = np.array(
    [[120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     #
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     #
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15],
     [120, 120, 60, 60, 40, 40, 30, 30, 24, 24, 20, 20, 17, 17, 15]]
)
price_transition_matrix_example = np.array(
    [[97, 100, 187, 166, 282, 348, 386, 404, 531, 540, 576, 647, 641, 651, 732],
     [81, 101, 217, 212, 282, 308, 401, 421, 506, 552, 620, 635, 721, 728, 727],
     [98, 86, 209, 181, 288, 278, 434, 406, 578, 484, 649, 642, 630, 644, 828],
     [98, 100, 203, 186, 310, 288, 395, 472, 462, 401, 622, 623, 766, 632, 848],
     [90, 102, 225, 196, 264, 276, 410, 363, 512, 549, 642, 588, 697, 739, 851],
     #
     [105, 117, 204, 214, 318, 328, 409, 416, 511, 508, 611, 568, 749, 739, 646],
     [94, 106, 187, 214, 351, 275, 356, 417, 455, 487, 606, 558, 759, 691, 761],
     [92, 109, 201, 180, 270, 287, 460, 384, 482, 491, 528, 570, 702, 744, 794],
     [107, 103, 167, 219, 279, 309, 398, 417, 549, 460, 706, 607, 709, 693, 816],
     [102, 90, 217, 202, 311, 327, 432, 371, 428, 455, 612, 618, 815, 767, 825],
     #
     [94, 93, 216, 195, 273, 275, 361, 423, 491, 529, 580, 668, 565, 742, 816],
     [108, 98, 203, 197, 313, 303, 388, 433, 455, 521, 650, 585, 707, 628, 925],
     [109, 101, 196, 209, 322, 257, 381, 377, 483, 528, 579, 658, 717, 829, 759],
     [103, 94, 200, 222, 296, 273, 409, 413, 547, 481, 563, 535, 758, 727, 804],
     [115, 109, 205, 212, 330, 309, 402, 321, 541, 478, 570, 631, 659, 736, 826]]
)
inventory_ratio_map = np.array(
    [[1000, 3],
     [11000, 4],
     [18600, 9],
     [31400, 21],
     [53000, 45],
     [116000, 99],
     [256000, 217],
     [562000, 478],
     [1240000, 1050],
     [2710000, 2310],
     [5960000, 3190],
     [13100000, 4070],
     [28800000, 7940],
     [28800000, 7940],
     [56200000, 15500],
     [110000000, 30300],
     [214000000, 59200],
     [419000000, 116000],
     [818000000, 226000],
     [1600000000, 441000],
     [3120000000, 861000],
     [6090000000, 1680000],
     [11900000000, 4110000],
     [23200000000, 10000000],
     [45400000000, 24500000],
     [111000000000, 93400000],
     [271000000000, 356000000],
     [661000000000, 1360000000],]
)

################## Optimization #####################
def generate_proposals(prices, inventory, max_cost, loc):
    price = prices[loc]
    n_goods = price.shape[0]
    if inventory is None:
        inventory = np.ones(n_goods) * 999999999999

    proposals = []
    for g1 in range(n_goods):
        num_g1 = min(max_cost // price[g1], inventory[g1])
        rest_cost = max_cost - num_g1 * price[g1]
        for g2 in range(n_goods):
            if g1 == g2:
                continue

            num_g2 = min(rest_cost // price[g2], inventory[g2])
            meta = dict()
            meta['location'] = loc
            meta[g1] = num_g1
            meta[g2] = num_g2

            num_vector = np.zeros(n_goods)
            num_vector[g1] = num_g1
            num_vector[g2] = num_g2

            inventory_ = inventory.copy()
            inventory_[g1] -= num_g1
            inventory_[g2] -= num_g2

            proposals.append((meta, num_vector, inventory_))

    return proposals

def maximize_profit_with_double_goods(prices, inventory, funds_init, loc_init=0, N=10, predefined_path=None):
    # prices: 价格矩阵
    # inventory: 库存矩阵
    # funds_init: 初始本金
    # loc_init:初始位置
    # N: 最大交易次数

    n_loc = prices.shape[0]
    n_goods = prices.shape[1]

    # dp[i][x][y] 表示第 i 次操作后位于地点 x 购买货物并且去往地点 y 出售所能获得的总资金
    dp = np.zeros((N + 1, n_loc, n_loc))
    dp[0] = funds_init

    dp_path = dict()
    for i in range(N + 1):
        for loc_base in range(n_loc):
            for loc_tgt in range(n_loc):
                dp_path[f'{i}_{loc_base}_{loc_tgt}'] = None

    dp_inventory = dict()
    for i in range(N + 1):
        for loc_base in range(n_loc):
            if i == 0 or (i == 1 and loc_base == loc_init):
                dp_inventory[f'{i}_{loc_base}'] = inventory
            else:
                dp_inventory[f'{i}_{loc_base}'] = None

    loc_greedy = None
    for i in range(N):
        loc_greedy_ = loc_greedy
        for loc_base in range(n_loc):
            if i == 0 and loc_base != loc_init:
                continue

            if inventory is not None and loc_greedy_ is not None and loc_base != loc_greedy_:
                continue

            fund_greedy = 0
            for loc_tgt in range(n_loc):
                if loc_base == loc_tgt:
                    continue

                funds_base = dp[i, loc_base, loc_tgt]
                inventory_base = dp_inventory[f'{i}_{loc_base}']
                if inventory_base is None:
                    inventory_base_ = None
                else:
                    inventory_base_ = inventory_base[loc_base]

                for proposal in generate_proposals(prices, inventory_base_, funds_base, loc_base):
                    meta, num_vector, inventory_new = proposal
                    cost = (prices[loc_base] * num_vector).sum()
                    revenue = (prices[loc_tgt] * num_vector).sum()
                    new_s = funds_base + (revenue - cost)

                    if new_s >= dp[i, loc_base, loc_tgt]:
                        dp_path[f'{i}_{loc_base}_{loc_tgt}'] = meta, num_vector
                        if inventory_base_ is not None:
                            inventory_base_new = inventory_base.copy()
                            inventory_base_new[loc_base] = inventory_new
                            dp_inventory[f'{i + 1}_{loc_tgt}'] = inventory_base_new

                    dp[i, loc_base, loc_tgt] = max(dp[i, loc_base, loc_tgt], new_s)
                    dp[i + 1, loc_tgt] = max(dp[i + 1, loc_tgt, 0], new_s)

                    if new_s >= fund_greedy:
                        fund_greedy = new_s
                        loc_greedy = loc_tgt
                        # print(f'{i} {loc_base} {loc_greedy}')

    return dp, dp_path
