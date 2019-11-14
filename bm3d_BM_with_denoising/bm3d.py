from utils import add_gaussian_noise, symetrize
from bm3d_BM_with_denoising.bm3d_1st_step_BM_with_denoising import bm3d_1st_step
from bm3d_2nd_step import bm3d_2nd_step
from psnr import compute_psnr

from denoising_method_NLM import nlm_denoise
from denoising_method_TV import tv_denoise
from denoising_method_Wavelet import wavelet_denoise


def run_bm3d(basic_denoising_im, noisy_im, sigma,
             n_H, k_H, N_H, p_H, tauMatch_H, useSD_H, tau_2D_H, lambda3D_H,
             n_W, k_W, N_W, p_W, tauMatch_W, useSD_W, tau_2D_W):
    k_H = 8 if (tau_2D_H == 'BIOR' or sigma < 40.) else 12
    k_W = 8 if (tau_2D_W == 'BIOR' or sigma < 40.) else 12

    noisy_im_p = symetrize(noisy_im, n_H)
    basic_denoising_im_p = symetrize(basic_denoising_im, n_H)
    img_basic = bm3d_1st_step(sigma, basic_denoising_im_p, noisy_im_p, n_H, k_H, N_H, p_H, lambda3D_H, tauMatch_H,
                              useSD_H, tau_2D_H)
    img_basic = img_basic[n_H: -n_H, n_H: -n_H]

    img_basic_p = symetrize(img_basic, n_W)
    noisy_im_p = symetrize(noisy_im, n_W)
    img_denoised = bm3d_2nd_step(sigma, noisy_im_p, img_basic_p, n_W, k_W, N_W, p_W, tauMatch_W, useSD_W, tau_2D_W)
    img_denoised = img_denoised[n_W: -n_W, n_W: -n_W]

    return img_basic, img_denoised


if __name__ == '__main__':
    import os
    import cv2
    import numpy as np

    # <hyper parameter> -------------------------------------------------------------------------------
    n_H = 16
    k_H = 8
    N_H = 16
    p_H = 3
    lambda3D_H = 2.7  # ! Threshold for Hard Thresholding
    useSD_H = False
    tau_2D_H = 'BIOR'

    n_W = 16
    k_W = 8
    N_W = 32
    p_W = 3
    useSD_W = True
    tau_2D_W = 'DCT'
    # <\ hyper parameter> -----------------------------------------------------------------------------

    im_dir = '../test_data/image'
    save_dir = 'result_image'
    os.makedirs(save_dir, exist_ok=True)
    for im_name in os.listdir(im_dir):
        # for im_name in ['Man.png',]:
        sigma_list = [2, 5, 10, 20, 30, 40, 60, 80, 100]
        for sigma in sigma_list:
            tauMatch_H = 2500 if sigma < 35 else 5000  # ! threshold determinates similarity between patches
            tauMatch_W = 400 if sigma < 35 else 3500  # ! threshold determinates similarity between patches
            noisy_dir = '../test_data/sigma' + str(sigma)

            im_path = os.path.join(im_dir, im_name)
            im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
            noisy_im_path = os.path.join(noisy_dir, im_name)
            noisy_im = cv2.imread(noisy_im_path, cv2.IMREAD_GRAYSCALE)

            basic_denoising_im = tv_denoise(noisy_im, sigma)

            im1, im2 = run_bm3d(basic_denoising_im, noisy_im, sigma,
                                n_H, k_H, N_H, p_H, tauMatch_H, useSD_H, tau_2D_H, lambda3D_H,
                                n_W, k_W, N_W, p_W, tauMatch_W, useSD_W, tau_2D_W)

            psnr_1st = compute_psnr(im, im1)
            psnr_2nd = compute_psnr(im, im2)

            im1 = (np.clip(im1, 0, 255)).astype(np.uint8)
            im2 = (np.clip(im2, 0, 255)).astype(np.uint8)

            save_name = im_name[:-4] + '-sigma_' + str(
                sigma) + '-1st' + '-TVdenoising' + '=PSNR_' + '%.4f' % psnr_1st + '.png'
            cv2.imwrite(os.path.join(save_dir, save_name), im1)
            save_name = im_name[:-4] + '-sigma_' + str(
                sigma) + '-2nd' + '-TVdenoising' + '=PSNR_' + '%.4f' % psnr_2nd + '.png'
            cv2.imwrite(os.path.join(save_dir, save_name), im2)
            print(os.path.join(save_dir, save_name))

    # NLM denoising
    for im_name in os.listdir(im_dir):
        # for im_name in ['Man.png',]:
        sigma_list = [2, 5, 10, 20, 30, 40, 60, 80, 100]
        for sigma in sigma_list:
            tauMatch_H = 2500 if sigma < 35 else 5000  # ! threshold determinates similarity between patches
            tauMatch_W = 400 if sigma < 35 else 3500  # ! threshold determinates similarity between patches
            noisy_dir = '../test_data/sigma' + str(sigma)

            im_path = os.path.join(im_dir, im_name)
            im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
            noisy_im_path = os.path.join(noisy_dir, im_name)
            noisy_im = cv2.imread(noisy_im_path, cv2.IMREAD_GRAYSCALE)

            basic_denoising_im = nlm_denoise(noisy_im, sigma)

            im1, im2 = run_bm3d(basic_denoising_im, noisy_im, sigma,
                                n_H, k_H, N_H, p_H, tauMatch_H, useSD_H, tau_2D_H, lambda3D_H,
                                n_W, k_W, N_W, p_W, tauMatch_W, useSD_W, tau_2D_W)

            psnr_1st = compute_psnr(im, im1)
            psnr_2nd = compute_psnr(im, im2)

            im1 = (np.clip(im1, 0, 255)).astype(np.uint8)
            im2 = (np.clip(im2, 0, 255)).astype(np.uint8)

            save_name = im_name[:-4] + '-sigma_' + str(
                sigma) + '-1st' + '-NLMdenoising' + '=PSNR_' + '%.4f' % psnr_1st + '.png'
            cv2.imwrite(os.path.join(save_dir, save_name), im1)
            save_name = im_name[:-4] + '-sigma_' + str(
                sigma) + '-2nd' + '-NLMdenoising' + '=PSNR_' + '%.4f' % psnr_2nd + '.png'
            cv2.imwrite(os.path.join(save_dir, save_name), im2)
            print(os.path.join(save_dir, save_name))

    # Wavelet denoising
    for im_name in os.listdir(im_dir):
        # for im_name in ['Man.png',]:
        sigma_list = [2, 5, 10, 20, 30, 40, 60, 80, 100]
        for sigma in sigma_list:
            tauMatch_H = 2500 if sigma < 35 else 5000  # ! threshold determinates similarity between patches
            tauMatch_W = 400 if sigma < 35 else 3500  # ! threshold determinates similarity between patches
            noisy_dir = '../test_data/sigma' + str(sigma)

            im_path = os.path.join(im_dir, im_name)
            im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
            noisy_im_path = os.path.join(noisy_dir, im_name)
            noisy_im = cv2.imread(noisy_im_path, cv2.IMREAD_GRAYSCALE)

            basic_denoising_im = wavelet_denoise(noisy_im, sigma)

            im1, im2 = run_bm3d(basic_denoising_im, noisy_im, sigma,
                                n_H, k_H, N_H, p_H, tauMatch_H, useSD_H, tau_2D_H, lambda3D_H,
                                n_W, k_W, N_W, p_W, tauMatch_W, useSD_W, tau_2D_W)

            psnr_1st = compute_psnr(im, im1)
            psnr_2nd = compute_psnr(im, im2)

            im1 = (np.clip(im1, 0, 255)).astype(np.uint8)
            im2 = (np.clip(im2, 0, 255)).astype(np.uint8)

            save_name = im_name[:-4] + '-sigma_' + str(
                sigma) + '-1st' + '-Wavelectdenoising' + '=PSNR_' + '%.4f' % psnr_1st + '.png'
            cv2.imwrite(os.path.join(save_dir, save_name), im1)
            save_name = im_name[:-4] + '-sigma_' + str(
                sigma) + '-2nd' + '-Wavelectdenoising' + '=PSNR_' + '%.4f' % psnr_2nd + '.png'
            cv2.imwrite(os.path.join(save_dir, save_name), im2)
            print(os.path.join(save_dir, save_name))

