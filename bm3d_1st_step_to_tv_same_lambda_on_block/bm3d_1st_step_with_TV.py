import numpy as np
import cv2

from utils import ind_initialize, get_kaiserWindow, sd_weighting
from precompute_BM import precompute_BM
from bior_2d import bior_2d_forward, bior_2d_reverse
from dct_2d import dct_2d_forward, dct_2d_reverse
from image_to_patches import image2patches
from build_3D_group import build_3D_group
from ht_filtering_hadamard import ht_filtering_hadamard
from trend_filtering_3D import trendFilter3D


def bm3d_1st_step_with_TV(sigma, img_noisy, nHard, kHard, NHard, pHard, lambdaHard3D, tauMatch, useSD, tau_2D, lamb):
    height, width = img_noisy.shape[0], img_noisy.shape[1]

    row_ind = ind_initialize(height - kHard + 1, nHard, pHard)
    column_ind = ind_initialize(width - kHard + 1, nHard, pHard)

    kaiserWindow = get_kaiserWindow(kHard)
    ri_rj_N__ni_nj, threshold_count = precompute_BM(img_noisy, kHW=kHard, NHW=NHard, nHW=nHard, tauMatch=tauMatch)
    for i in range(height):
        for j in range(width):
            assert ri_rj_N__ni_nj[i][j][0][0] == i
            assert ri_rj_N__ni_nj[i][j][0][1] == j
    group_len = int(np.sum(threshold_count))
    group_3D_table = np.zeros((group_len, kHard, kHard))
    weight_table = np.zeros((height, width))

    all_patches = image2patches(img_noisy, k=kHard, p=pHard)  # i_j_ipatch_jpatch__v
    if tau_2D == 'DCT':
        fre_all_patches = dct_2d_forward(all_patches)
    elif tau_2D == 'BIOR':  # 'BIOR'
        fre_all_patches = bior_2d_forward(all_patches)
    else:
        fre_all_patches = all_patches
    fre_all_patches = fre_all_patches.reshape((height - kHard + 1, height - kHard + 1, kHard, kHard))

    acc_pointer = 0
    for i_r in row_ind:
        for j_r in column_ind:
            nSx_r = threshold_count[i_r, j_r]
            group_3D = build_3D_group(fre_all_patches, ri_rj_N__ni_nj[i_r, j_r], nSx_r)
            group_3D_temp, weight = ht_filtering_hadamard(group_3D, sigma, lambdaHard3D, not useSD)
            group_3D = trendFilter3D(group_3D, lamb)
            group_3D = group_3D.transpose((2, 0, 1))
            group_3D_table[acc_pointer:acc_pointer + nSx_r] = group_3D
            acc_pointer += nSx_r

            if useSD:
                weight = sd_weighting(group_3D)

            weight_table[i_r, j_r] = weight

    if tau_2D == 'DCT':
        group_3D_table = dct_2d_reverse(group_3D_table)
    elif tau_2D == 'BIOR':  # 'BIOR'
        group_3D_table = bior_2d_reverse(group_3D_table)
    else:
        group_3D_table *= kaiserWindow

    numerator = np.zeros_like(img_noisy, dtype=np.float64)
    denominator = np.zeros((img_noisy.shape[0] - 2 * nHard, img_noisy.shape[1] - 2 * nHard), dtype=np.float64)
    denominator = np.pad(denominator, nHard, 'constant', constant_values=1.)
    acc_pointer = 0
    for i_r in row_ind:
        for j_r in column_ind:
            nSx_r = threshold_count[i_r, j_r]
            N_ni_nj = ri_rj_N__ni_nj[i_r, j_r]
            group_3D = group_3D_table[acc_pointer:acc_pointer + nSx_r]
            acc_pointer += nSx_r
            weight = weight_table[i_r, j_r]
            for n in range(nSx_r):
                ni, nj = N_ni_nj[n]
                patch = group_3D[n]
                if tau_2D == 'DCT' or tau_2D == 'BIOR':
                    numerator[ni:ni + kHard, nj:nj + kHard] += patch * kaiserWindow * weight
                    denominator[ni:ni + kHard, nj:nj + kHard] += kaiserWindow * weight
                elif tau_2D == 'TV':
                    numerator[ni:ni + kHard, nj:nj + kHard] += patch * weight
                    denominator[ni:ni + kHard, nj:nj + kHard] += kaiserWindow * weight

    img_basic = numerator / denominator
    return img_basic