import numpy as np
import cv2


def compute_patch_distance(im, k, refer_center=None):
    assert k % 2 == 1
    im_h, im_w = im.shape
    if refer_center == None:
        cy, cx = im_h // 2, im_w // 2
    else:
        cy, cx = refer_center
    im = im.astype(np.float64)
    distance_table = np.zeros((im_h - k + 1, im_w - k + 1), np.float64)
    refer_patch = im[cy - k // 2:cy + k // 2 + 1, cx - k // 2: cx + k // 2 + 1]

    for i in range(k // 2, im_h - k // 2):
        for j in range(k // 2, im_w - k // 2):
            relative_patch = im[i - k // 2:i + k // 2 + 1, j - k // 2: j + k // 2 + 1]
            distance = np.sum((refer_patch - relative_patch) * (refer_patch - relative_patch)) / k / k
            distance_table[i - k // 2][j - k // 2] = distance

    return distance_table


def distance2weight(distance, h=10):
    weight_table = distance / (h * h)
    weight_table = np.power(np.e, -weight_table)
    weight_table = weight_table / np.sum(weight_table)
    weight_table = weight_table / np.max(weight_table)
    weight_table = weight_table * 255
    weight_table = weight_table.astype(np.uint8)
    return weight_table


if __name__ == '__main__':
    import os

    read_dir = 'special_test_image'
    save_dir = 'weight_res_show'
    for im_name in os.listdir(read_dir):
        im_path = os.path.join(read_dir, im_name)
        im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
        distance_table = compute_patch_distance(im, 9)
        weight_table = distance2weight(distance_table)
        cv2.imwrite(os.path.join(save_dir, im_name), weight_table)
