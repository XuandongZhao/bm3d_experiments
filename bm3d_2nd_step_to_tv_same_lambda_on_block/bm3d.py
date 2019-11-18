import numpy as np
import cv2
import prox_tv as ptv

from utils import ind_initialize, get_kaiserWindow, sd_weighting
from precompute_BM import precompute_BM
from bior_2d import bior_2d_forward, bior_2d_reverse
from dct_2d import dct_2d_forward, dct_2d_reverse
from image_to_patches import image2patches
from build_3D_group import build_3D_group
from trend_filtering_3D import trendFilter3D


def bm3d_2nd_step_trendfilter3D(img_noisy, img_basic, nWien, kWien, NWien, pWien, tauMatch, useSD, lamb):
    height, width = img_noisy.shape[0], img_noisy.shape[1]

    row_ind = ind_initialize(height - kWien + 1, nWien, pWien)
    column_ind = ind_initialize(width - kWien + 1, nWien, pWien)

    kaiserWindow = get_kaiserWindow(kWien)
    ri_rj_N__ni_nj, threshold_count = precompute_BM(img_basic, kHW=kWien, NHW=NWien, nHW=nWien, tauMatch=tauMatch)
    group_len = int(np.sum(threshold_count))
    group_3D_table = np.zeros((group_len, kWien, kWien))
    weight_table = np.ones((height, width))

    noisy_patches = image2patches(img_noisy, k=kWien, p=pWien)  # i_j_ipatch_jpatch__v
    basic_patches = image2patches(img_basic, k=kWien, p=pWien)  # i_j_ipatch_jpatch__v

    noisy_patches = noisy_patches.reshape((height - kWien + 1, height - kWien + 1, kWien, kWien))
    basic_patches = basic_patches.reshape((height - kWien + 1, height - kWien + 1, kWien, kWien))

    acc_pointer = 0
    for i_r in row_ind:
        for j_r in column_ind:
            nSx_r = threshold_count[i_r, j_r]
            group_3D_est = build_3D_group(noisy_patches, ri_rj_N__ni_nj[i_r, j_r], nSx_r)
            group_3D = trendFilter3D(group_3D_est, lamb)
            group_3D = group_3D.transpose((2, 0, 1))

            group_3D_table[acc_pointer:acc_pointer + nSx_r] = group_3D
            acc_pointer += nSx_r

            # if useSD:
            weight = sd_weighting(group_3D)
            weight_table[i_r, j_r] = weight

    group_3D_table *= kaiserWindow

    numerator = np.zeros_like(img_noisy, dtype=np.float64)
    denominator = np.zeros_like(img_noisy, dtype=np.float64)
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

                numerator[ni:ni + kWien, nj:nj + kWien] += patch * weight
                denominator[ni:ni + kWien, nj:nj + kWien] += kaiserWindow * weight

    img_denoised = numerator / denominator
    return img_denoised


if __name__ == '__main__':
    from psnr import compute_psnr
    from utils import add_gaussian_noise, symetrize
    from bm3d_1st_step import bm3d_1st_step
    import os

    # <hyper parameter> -------------------------------------------------------------------------------
    sigma = 20

    nHard = 16
    kHard = 8
    NHard = 16
    pHard = 3
    lambdaHard3D = 2.7  # ! Threshold for Hard Thresholding
    tauMatchHard = 2500 if sigma < 35 else 5000  # ! threshold determinates similarity between patches
    useSD_h = False
    tau_2D_hard = 'BIOR'
    # <\ hyper parameter> -----------------------------------------------------------------------------

    img = cv2.imread('../test_data/image/Lena.png', cv2.IMREAD_GRAYSCALE)
    im_name = 'Lena.png'
    save_dir = './result_images/'
    img = cv2.resize(img, (256, 256))
    img_noisy = add_gaussian_noise(img, sigma, seed=0)

    img_noisy_p = symetrize(img_noisy, nHard)
    img_basic = bm3d_1st_step(sigma, img_noisy_p, nHard, kHard, NHard, pHard, lambdaHard3D, tauMatchHard, useSD_h,
                              tau_2D_hard)
    img_basic = img_basic[nHard: -nHard, nHard: -nHard]

    # <hyper parameter> -------------------------------------------------------------------------------
    sigma = 20

    nWien = 16
    kWien = 8
    NWien = 16
    pWien = 3
    tauMatchWien = 400 if sigma < 35 else 3500  # ! threshold determinates similarity between patches
    useSD_w = True

    for lamb in [8]:
        # for lamb3 in [1, 2, 3, 4, 6, 7, 8, 9, 10, 20, 30, 40]:
        for lamb3 in [7, 8, 9]:
            slamb = (8, 8, lamb3)
            # lamb = 1
            # <\ hyper parameter> -----------------------------------------------------------------------------

            img_basic_p = symetrize(img_basic, nWien)
            img_noisy_p = symetrize(img_noisy, nWien)
            img_denoised = bm3d_2nd_step_trendfilter3D(img_noisy_p, img_basic_p, nWien, kWien, NWien, pWien,
                                                       tauMatchWien,
                                                       useSD_w, slamb)
            img_denoised = img_denoised[nWien: -nWien, nWien: -nWien]

            psnr_2st = compute_psnr(img, img_denoised)
            dif_img = np.abs(img_denoised - img)
            dif_img = np.clip(dif_img, 0, 255)
            dif_img = dif_img.astype(np.uint8)
            img_denoised = (np.clip(img_denoised, 0, 255)).astype(np.uint8)

            print('img and img_denoised PSNR: ', psnr_2st)
            cv2.imwrite('y_final.png', img_denoised)

            save_name = im_name[:-4] + '_s' + str(sigma) + '_2_lam_' + str(lamb3) + '_P' + str(
                round(psnr_2st, 3)) + '.png'
            cv2.imwrite(os.path.join(save_dir, save_name), img_denoised)
            save_res_name = im_name[:-4] + '_s' + str(sigma) + '_2_lam_' + str(lamb) + '_py_dif.png'
            cv2.imwrite(os.path.join(save_dir, save_res_name), dif_img)
