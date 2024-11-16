import os
import argparse
import pandas as pd
from tqdm import tqdm
from xyst_utils import *

parser = argparse.ArgumentParser()
parser.add_argument('--data_path', type=str, default='./data/example_data.xlsx')
# parser.add_argument('--inventory_ratio', default=3)
parser.add_argument('--funds_init', type=int, default=6800)
parser.add_argument('--num_trans', type=int, default=13)
parser.add_argument('--save_path', type=str, default='./output')
parser.add_argument('--out_name', type=str, default=None)
parser.add_argument('--greedy', action='store_true')
parser.add_argument('--greedy_constraint', action='store_true')
args = parser.parse_args()

os.makedirs(args.save_path, exist_ok=True)
out_name = f'{args.funds_init}_{args.num_trans}' if args.out_name is None else args.out_name
if args.greedy:
    out_file = open(os.path.join(args.save_path, f'{out_name}_greedy.txt'), mode='w', encoding='utf-8')
else:
    out_file = open(os.path.join(args.save_path, f'{out_name}.txt'), mode='w', encoding='utf-8')

price_transition_matrix = pd.read_excel(args.data_path)
price_transition_matrix = np.array(price_transition_matrix.iloc[:, 1:])
funds_init = args.funds_init
N = args.num_trans

ship_level_init = (inventory_ratio_map[:, 0] < funds_init).sum()
inventory_ratio_init = inventory_ratio_map[ship_level_init - 1, 1]
inventory_matrix_init = base_inventory * inventory_ratio_init

num_loc = len(locations)
num_goods = len(goods)

out_file.write('Copyright (c) 2024 大眼松鼠. All rights reserved.\n\n')
out_file.write(f'初始资金{funds_init}，库存倍率{inventory_ratio_init}，共跑{args.num_trans}次\n')
out_file.write(f'因初始资金和库存不同，购买数量参考价值有限，默认第一种买满，剩余资金第二种买满\n')
out_file.write(f'注：是否停止加速应和飞行舟等级结合判断，若到达后升级，可在刷新库存前1分钟加速，待刷新后再出发\n')
out_file.write(f'若如此做，请根据更新的初始条件重跑此程序或联系作者\n\n')

for loc_init in tqdm(range(num_loc)):
    if args.greedy:
        inventory_input = base_inventory * 9999999999999999999999999999999
    elif args.greedy_constraint:
        inventory_input = inventory_matrix_init
    else:
        inventory_input = None
    sol, sol_path, sol_inventory = maximize_profit_with_double_goods(
        price_transition_matrix, inventory_input, funds_init, loc_init, N
    )


    i = N - 1
    loc_final = sol[N,:,0].argmax()
    sol_loc = [loc_final]
    sol_goods = []
    sol_money = []
    while i > 0:
        loc_pre = sol[i, :, loc_final].argmax()
        sol_loc.append(loc_pre)
        sol_goods.append(sol_path[f'{i}_{loc_pre}_{loc_final}'])
        sol_money.append(sol[i, loc_pre, loc_final])
        i -= 1
        loc_final = loc_pre
    sol_goods.append(sol_path[f'{i}_{loc_init}_{loc_final}'])
    sol_money.append(sol[i, loc_init, loc_final])

    out_file.write(f'### 初始{locations[loc_init]}:\n')
    num_vector_total = np.zeros_like(inventory_matrix_init) * 1.0
    inventory_matrix_rest = np.zeros_like(inventory_matrix_init) * 1.0
    inventory_matrix_rest_for_over_inventory = np.zeros_like(inventory_matrix_init) * 1.0
    over_inventory = False
    num_transaction = 0
    stop_transaction = 0

    ship_level_real = ship_level_init
    inventory_ratio_real = inventory_ratio_init
    inventory_matrix_real = inventory_matrix_init
    for i in np.arange(N)[::-1]:
        goods_policy = ''
        meta, num_vector = sol_goods[i]

        for idx, g in enumerate(meta.keys()):
            if g == 'location':
                num_vector_total[meta[g]] += num_vector
                if (num_vector_total > inventory_matrix_real).any():
                    inventory_matrix_rest = inventory_matrix_real - num_vector_total
                    inventory_matrix_rest[meta[g]] += num_vector
                    out_file.write(
                        f'**第{num_transaction}次发船后因超库存建议停止加速，以下策略为刷新库存后，库存倍率{inventory_ratio_real}**\n'
                    )

                    if not over_inventory:
                        over_inventory = True
                        inventory_matrix_rest_for_over_inventory = inventory_matrix_rest.copy()
                        stop_transaction = num_transaction - 1

                    inventory_matrix_real = base_inventory * inventory_ratio_real
                    num_vector_total = np.zeros_like(inventory_matrix_init) * 1.0
                    inventory_matrix_rest = np.zeros_like(inventory_matrix_init) * 1.0
            else:
                goods_name = goods[g]
                goods_num = int(meta[g])
                if goods_num > 0:
                    goods_policy += f'{goods_name}:{goods_num}'
                    if idx < len(meta.keys()) - 1:
                        goods_policy += ', '

        if num_transaction > 0:
            out_file.write(f'到达后资金{int(sol_money[i+1])}')

            ship_level_cur = (inventory_ratio_map[:, 0] < sol_money[i+1]).sum()
            if ship_level_cur > ship_level_real:
                ship_level_real = ship_level_cur
                inventory_ratio_real = inventory_ratio_map[ship_level_cur - 1, 1]
                out_file.write(f'，飞行舟升级，当前库存倍率{inventory_ratio_real}')
            out_file.write('\n')

        num_transaction += 1
        out_file.write(f'第{num_transaction}次发船: ({goods_policy})->{locations[sol_loc[i]]}\n')

    out_file.write(f'到达后资金{int(sol_money[i])}')
    ship_level_cur = (inventory_ratio_map[:, 0] < sol_money[i]).sum()
    if ship_level_cur > ship_level_real:
        ship_level_real = ship_level_cur
        inventory_ratio_real = inventory_ratio_map[ship_level_cur - 1, 1]
        out_file.write(f'，飞行舟升级，当前库存倍率{inventory_ratio_real}')
    out_file.write('\n\n')

    ############### over inventory #################
    if over_inventory:
        out_file.write(f'第{stop_transaction + 1}次发船后超库存策略，如此请根据更新的初始条件重跑此程序或联系作者\n')

        meta, num_vector = sol_goods[::-1][stop_transaction + 1]
        loc_init_ = meta['location']
        funds_init_ = np.array(sol_money)[::-1][stop_transaction]
        inventory_matrix_ = inventory_matrix_rest_for_over_inventory
        N_ = 4

        out_file.write(f'初始位置{locations[loc_init_]}, 资金{int(funds_init_)}\n')
        sol, sol_path, sol_inventory = maximize_profit_with_double_goods(
            price_transition_matrix, inventory_matrix_, funds_init_, loc_init_, N_
        )

        i = N_ - 1
        loc_final = sol[N_, :, 0].argmax()
        sol_loc = [loc_final]
        sol_goods = []
        sol_money = []
        while i > 0:
            loc_pre = sol[i, :, loc_final].argmax()
            sol_loc.append(loc_pre)
            sol_goods.append(sol_path[f'{i}_{loc_pre}_{loc_final}'])
            sol_money.append(sol[i, loc_pre, loc_final])
            i -= 1
            loc_final = loc_pre
        sol_goods.append(sol_path[f'{i}_{loc_init_}_{loc_final}'])
        sol_money.append(sol[i, loc_init_, loc_final])

        num_transaction = stop_transaction + 1
        for i in np.arange(N_)[::-1]:
            goods_policy = ''
            meta, num_vector = sol_goods[i]
            for idx, g in enumerate(meta.keys()):
                if g == 'location':
                    continue
                else:
                    goods_name = goods[g]
                    goods_num = int(meta[g])
                    if goods_num > 0:
                        goods_policy += f'{goods_name}:{goods_num}'
                        if idx < len(meta.keys()) - 1:
                            goods_policy += ', '

            num_transaction += 1
            out_file.write(f'第{num_transaction}次发船: ({goods_policy})->{locations[sol_loc[i]]}\n')
            out_file.write(f'到达后资金{int(sol_money[i])}\n')
        out_file.write('\n')

out_file.close()
