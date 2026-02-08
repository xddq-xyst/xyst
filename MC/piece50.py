import numpy as np
from tqdm import tqdm

def select(N, N_box=5, N_pieces=50):
    random_array = np.random.rand(N, 9)
    result = np.argsort(random_array, axis=1)[:, :N_box]

    piece1 = np.any(result == 0, axis=1)
    piece3 = np.any(result == 1, axis=1)

    piece = np.cumsum(piece1 + piece3 * 3)
    time = (piece < N_pieces).sum() + 1

    return time


N_pieces = 50
N_boxes = [3, 4, 5, 6, 7, 8]
N = 100
N_exp = 100000
for m in N_boxes:
    times = []
    for i in tqdm(range(N_exp)):
        time = select(N, N_box=m, N_pieces=N_pieces)
        times.append(time)
    times = np.asarray(times)
    quantiles = np.quantile(times, [0.1, 0.25, 0.5, 0.75, 0.9])
    print(times.mean())
    print(quantiles)
