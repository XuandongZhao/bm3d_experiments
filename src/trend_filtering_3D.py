import numpy as np
import prox_tv as ptv
from utils import add_gaussian_noise


def trendFilter3D(tensor, lamb, k=0):
    if isinstance(lamb, tuple):
        lamb_x, lamb_y, lamb_z = lamb[0], lamb[1], lamb[2]
    else:
        lamb_x = lamb
        lamb_y = lamb
        lamb_z = lamb

    if k == 0:
        filtered_block = ptv.tvgen(tensor, [lamb_x, lamb_y, lamb_z], [1, 2, 3], [1, 1, 1])
    elif k == 1:
        pass
    elif k == 2:
        pass
    else:
        raise NotImplementedError

    return filtered_block


if __name__ == '__main__':
    import cv2
    import time

    block = np.ones((64, 64, 16)) * 128
    block = add_gaussian_noise(block, 50)

    tik = time.time()

    res = trendFilter3D(block, 10, k=0)

    print(time.time() - tik)

    res_im = res.astype(np.uint8)

    for i in range(16):
        slice = res_im[:, i, :]
