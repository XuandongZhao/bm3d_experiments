import cv2


def nlm_denoise(noisy_im, sigma):
    if sigma == 2:
        h = 2.0263157894736836
    elif sigma == 5:
        h = 5.355263157894737
    elif sigma == 10:
        h = 10.473684210526315
    elif sigma == 20:
        h = 18.894736842105264
    elif sigma == 30:
        h = 25.894736842105264
    elif sigma == 40:
        h = 32.21052631578947
    elif sigma == 60:
        h = 43.10526315789474
    elif sigma == 80:
        h = 53.26315789473684
    elif sigma == 100:
        h = 61.578947368421055
    else:
        print('false')

    im_est = cv2.fastNlMeansDenoising(noisy_im, None, h=h, templateWindowSize=7, searchWindowSize=21)
    return im_est


if __name__ == '__main__':
    import numpy as np
    from utils import add_gaussian_noise

    sigma = 40
    im = cv2.imread('test_image/Cameraman.png', cv2.IMREAD_GRAYSCALE)
    noisy_im = add_gaussian_noise(im, sigma)
    # cv2.imshow('noisy_im', noisy_im)

    im_est = nlm_denoise(noisy_im, sigma)
    cv2.imwrite('im_est.png', im_est)

# if __name__ == '__main__':
#     from BM3D.utils import add_gaussian_noise
#     from BM3D.psnr import compute_psnr
#     from utils import draw_two_list
#     import os
#     import numpy as np
#
#     #              # h
#     # sigma = 2    # 2.0263157894736836
#     # sigma = 5    # 5.355263157894737
#     # sigma = 10   # 10.473684210526315
#     # sigma = 20   # 18.894736842105264
#     # sigma = 30   # 25.894736842105264
#     # sigma = 40   # 32.21052631578947
#     # sigma = 60   # 43.10526315789474
#     # sigma = 80   # 53.26315789473684
#     # sigma = 100  # 61.578947368421055
#
#     save_dir = 'NLM_denoising_image'
#     os.makedirs(save_dir, exist_ok=True)
#     hyper_estimate_list = list()
#     # for sigma in [2, 5, 10, 20, 30, 40, 60, 80, 100]:
#     for sigma in [100]:
#         test_im_dir = 'test_image'
#         max_psnr_h = list()
#         for im_name in os.listdir(test_im_dir):
#             im_path = os.path.join(test_im_dir, im_name)
#             im = cv2.imread(im_path)
#             noisy_im = add_gaussian_noise(im, sigma, seed=1)
#
#             h_list = np.arange(0, 20) * sigma / 10
#             psnr_list = list()
#             for h in h_list:
#                 im_est = cv2.fastNlMeansDenoising(noisy_im, None, h=h, templateWindowSize=7, searchWindowSize=21)
#                 psnr = compute_psnr(im, im_est)
#                 psnr_list.append(psnr)
#             max_psnr_h.append(np.argmax(psnr_list) * sigma / 10)
#             draw_two_list(h_list, psnr_list, os.path.join(save_dir, im_name))
#             print(os.path.join(save_dir, im_name))
#         print(sigma, ': max_psnr_h', max_psnr_h)
#         mean_h = np.mean(max_psnr_h)
#         print(sigma, ': ', mean_h)
#     hyper_estimate_list.append(mean_h)
#     print(hyper_estimate_list)
