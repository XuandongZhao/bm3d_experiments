import cv2
import os
import numpy as np
import scipy.sparse as sp
from utils import add_gaussian_noise


def gtf_admm_v2(y, D, k, lamda, rho, varargin):
    flag = 0 if k % 4 == 0 else 1
    n = len(y)
    m = D.shape[0]
    if (D.shape[1] == 2):
        edges1 = D[:, 0]
        edges2 = D[:, 1]
        D = sp.csr_matrix((edges1, edges2), shape=(m, n))
    else:
        edges1 = np.zeros((m, 1))
        edges2 = np.zeros((m, 1))


    if k==0:
        print('Direct Solution:')


if __name__ == '__main__':
    im_path = './test_data/original_image/Alley.png'
    im = cv2.imread(im_path)
    if im.ndim == 3:
        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    sigma = 20
    im_noise = add_gaussian_noise(im, sigma, seed=0)
    print(im.shape)
    ht, wt = im.shape
    n = ht * wt
    m = (n * 4 - 2 * (ht + wt)) / 2
    edge1 = np.zeros((m, 1))
    edge2 = np.zeros((m, 1))
