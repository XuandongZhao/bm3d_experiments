import pyct
from pyct.fdct2 import fdct2
from pyct.fdct3 import fdct3


def curvelet_2d_forward(img):
    return img


def curvelet_2d_reverse(img):
    return img


if __name__ == '__main__':
    import cv2
    import numpy as np

    im = cv2.imread('../test_data/image/Alley.png', cv2.IMREAD_GRAYSCALE)
    im = im.astype(np.float64)
    # fre_im = dct_2d_forward(im)
    # im_ = dct_2d_reverse(fre_im)

    A = fdct2(im.shape, 6, 32, True, cpx=True)
    fre_im = A.fwd(im)
    im_ = A.inv(fre_im)

    diff = np.abs(im - im_)

    print(np.max(diff))
    print(np.sum(diff))
    im_ = im_.astype(np.uint8)
    cv2.imshow('im_', im_)
    cv2.waitKey()
