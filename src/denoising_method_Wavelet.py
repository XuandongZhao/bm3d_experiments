import cv2
import numpy as np
from skimage.restoration import denoise_wavelet


def wavelet_denoise(noisy_im):
    im_est = denoise_wavelet(noisy_im, method='BayesShrink', mode='soft', rescale_sigma=True)
    im_est = np.clip(im_est * 255, 0, 255)
    im_est = im_est.astype(np.uint8)
    return im_est


if __name__ == '__main__':
    from utils import add_gaussian_noise

    sigma = 40
    im = cv2.imread('test_image/Cameraman.png', cv2.IMREAD_GRAYSCALE)
    noisy_im = add_gaussian_noise(im, sigma)

    im_est = wavelet_denoise(noisy_im)
    cv2.imwrite('im_est.png', im_est)
