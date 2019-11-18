import os
from GEAR.res_name_dencode import decode_res

standard_result_dir = '../RESULT_bm3d_standard'


def get_standard_result(im_name, sigma):
    for name in os.listdir(standard_result_dir):
        if im_name[:-4] in name and 'sigma_' + str(int(sigma)) + '-' in name:
            if '-1st' in name:
                res_1st = decode_res(name)
            if '-2nd' in name:
                res_2nd = decode_res(name)
    res_1st = float(res_1st['PSNR'])
    res_2nd = float(res_2nd['PSNR'])
    return res_1st, res_2nd


if __name__ == '__main__':
    im_name = 'Cameraman.png'
    sigma = 40
    a = get_standard_result(im_name, sigma)
    print(a)
