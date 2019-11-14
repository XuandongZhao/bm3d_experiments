import cv2
import prox_tv as ptv


def tv_denoise(noisy_im, sigma):
    if sigma == 2:
        weight = 0.38828571428571435
    elif sigma == 5:
        weight = 1.7
    elif sigma == 10:
        weight = 4.228571428571429
    elif sigma == 20:
        weight = 10.857142857142858
    elif sigma == 30:
        weight = 19.142857142857142
    elif sigma == 40:
        weight = 24.857142857142858
    elif sigma == 60:
        weight = 38.857142857142854
    elif sigma == 80:
        weight = 48.857142857142854
    elif sigma == 100:
        weight = 56.0
    else:
        print('false')

    im_est = ptv.tv1_2d(noisy_im, w=weight)
    return im_est


if __name__ == '__main__':
    import numpy as np
    from utils import add_gaussian_noise

    sigma = 40
    im = cv2.imread('../test_data/image/Cameraman.png', cv2.IMREAD_GRAYSCALE)
    noisy_im = add_gaussian_noise(im, sigma)
    # cv2.imshow('noisy_im', noisy_im)

    im_est = tv_denoise(noisy_im, sigma)
    cv2.imwrite('im_est.png', im_est)



# if __name__ == '__main__':
#     from BM3D.utils import add_gaussian_noise
#     from BM3D.psnr import compute_psnr
#     from utils import draw_two_list
#     import os
#     import numpy as np
#
#     #              # weight
#     # sigma = 2    # 0.38828571428571435
#     # sigma = 5    # 1.7
#     # sigma = 10   # 4.228571428571429
#     # sigma = 20   # 10.857142857142858
#     # sigma = 30   # 19.142857142857142
#     # sigma = 40   # 24.857142857142858
#     # sigma = 60   # 38.857142857142854
#     # sigma = 80   # 48.857142857142854
#     # sigma = 100  # 56.0
#
#     hyper_estimate_list = list()
#     for sigma in [2, 5, 10, 20, 30, 40, 60, 80, 100]:
#
#         test_im_dir = 'test_image'
#         save_dir = 'TV_denoising'
#         os.makedirs(save_dir, exist_ok=True)
#         max_psnr_hyper_list = list()
#         for im_name in os.listdir(test_im_dir):
#             im_path = os.path.join(test_im_dir, im_name)
#             im = cv2.imread(im_path)
#             noisy_im = add_gaussian_noise(im, sigma, seed=1)
#
#             # hyper_list = (np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])[np.newaxis, :] * np.power(10., np.arange(-2, 3))[:,
#             #                                                                      np.newaxis]).flatten()
#             hyper_list = (np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])[np.newaxis, :] * np.power(10., np.arange(-2, 3))[:,
#                                                                                  np.newaxis]).flatten()
#             # hyper_list = np.arange(45, 80)
#             psnr_list = list()
#             for hyper in hyper_list:
#                 im_est = ptv.tv1_2d(noisy_im, w=hyper)
#                 # im_est = denoise_tv_chambolle(noisy_im, weight=hyper)
#                 psnr = compute_psnr(im, im_est)
#                 psnr_list.append(psnr)
#             max_psnr_hyper = hyper_list[np.argmax(psnr_list)]
#             max_psnr_hyper_list.append(max_psnr_hyper)
#             draw_two_list(hyper_list, psnr_list, os.path.join(save_dir, im_name), log=True)
#             print(os.path.join(save_dir, im_name))
#             print(max_psnr_hyper)
#         print(sigma, ': max_psnr_hyper_list', max_psnr_hyper_list)
#         mean = np.mean(max_psnr_hyper_list)
#         print('mean:  ', mean)
#         hyper_estimate_list.append(mean)
#     print(hyper_estimate_list)
