import os
from plot_list_dict import plot_dict_res
from GEAR.res_name_dencode import find_filename_in_dir, decode_res

if __name__ == '__main__':
    im_name_list = ['Alley.png', 'Baboon.png', 'barbara.png', 'boat.png', 'Book.png', 'Building1.png', 'Building2.png',
                    'Cameraman.png', 'Computer.png', 'couple.png', 'Dice.png', 'F16.png', 'fingerprint.png',
                    'Flowers1.png', 'Flowers2.png', 'Gardens.png', 'Girl.png', 'Hallway.png', 'hill.png', 'house.png',
                    'Lena.png', 'Man.png', 'Man1.png', 'Man2.png', 'montage.png', 'pentagon.png', 'peppers.png',
                    'Plaza.png', 'Statue.png', 'Street1.png', 'Street2.png', 'Traffic.png', 'Trees.png',
                    'Valldemossa.png', 'Yard.png']

    input_dir = 'result_images'
    save_dir = 'result_compare'
    os.makedirs(save_dir, exist_ok=True)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    search_dir = os.path.join(current_dir, input_dir)

    # 1st step result compare
    for im_name in im_name_list:
        DCT_1st_list = list()
        BIOR_1st_list = list()

        im_str = im_name[:-4]

        sigma_list = [2, 5, 10, 20, 30, 40, 60, 80, 100]
        for sigma in sigma_list:
            sigma_str = 'sigma_' + str(sigma)

            name = find_filename_in_dir(search_dir,
                                        include_str_list=(im_str, sigma_str, '1st_DCT'),
                                        exclude_str_list=('2nd'))
            psnr = decode_res(name)['PSNR']
            DCT_1st_list.append(psnr)

            name = find_filename_in_dir(search_dir,
                                        include_str_list=(im_str, sigma_str, '1st_BIOR'),
                                        exclude_str_list=('2nd'))
            psnr = decode_res(name)['PSNR']
            BIOR_1st_list.append(psnr)

        x_list = sigma_list
        y_list = DCT_1st_list
        k_ = ['name', 'x', 'y', 'color', 'linestyle']
        v_ = ['BIOR_1st', x_list, y_list, 'green', '--']
        line_dict_1 = dict(zip(k_, v_))

        x_list = sigma_list
        y_list = DCT_1st_list
        k_ = ['name', 'x', 'y', 'color', 'linestyle']
        v_ = ['DCT_1st', x_list, y_list, 'red', '--']
        line_dict_2 = dict(zip(k_, v_))

        plt = plot_dict_res(line_dict_1, line_dict_2, x_lable='sigma', y_label='PSNR', im_label=im_name)

    # 2nd step result compare
    for im_name in im_name_list:
        BIOR_1st_BIOR_2nd_list = list()
        BIOR_1st_DCT_2nd_list = list()
        DCT_1st_DCT_2nd_list = list()
        DCT_1st_BIOR_2nd_list = list()

        im_str = im_name[:-4]

        sigma_list = [2, 5, 10, 20, 30, 40, 60, 80, 100]
        for sigma in sigma_list:
            sigma_str = 'sigma_' + str(sigma)

            name = find_filename_in_dir(search_dir, include_str_list=(im_str, sigma_str, '1st_BIOR', '2nd_BIOR'))
            psnr = decode_res(name)['PSNR']
            BIOR_1st_BIOR_2nd_list.append(psnr)

            name = find_filename_in_dir(search_dir, include_str_list=(im_str, sigma_str, '1st_BIOR', '2nd_DCT'))
            psnr = decode_res(name)['PSNR']
            BIOR_1st_DCT_2nd_list.append(psnr)

            name = find_filename_in_dir(search_dir, include_str_list=(im_str, sigma_str, '1st_DCT', '2nd_DCT'))
            psnr = decode_res(name)['PSNR']
            DCT_1st_DCT_2nd_list.append(psnr)

            name = find_filename_in_dir(search_dir, include_str_list=(im_str, sigma_str, '1st_DCT', '2nd_BIOR'))
            psnr = decode_res(name)['PSNR']
            DCT_1st_BIOR_2nd_list.append(psnr)

        x_list = sigma_list
        y_list = BIOR_1st_BIOR_2nd_list
        k_ = ['name', 'x', 'y', 'color', 'linestyle']
        v_ = ['BIOR_1st_BIOR_2nd', x_list, y_list, 'yellow', '--']
        line_dict_1 = dict(zip(k_, v_))

        x_list = sigma_list
        y_list = BIOR_1st_DCT_2nd_list
        k_ = ['name', 'x', 'y', 'color', 'linestyle']
        v_ = ['BIOR_1st_DCT_2nd', x_list, y_list, 'green', '--']
        line_dict_2 = dict(zip(k_, v_))

        x_list = sigma_list
        y_list = DCT_1st_DCT_2nd_list
        k_ = ['name', 'x', 'y', 'color', 'linestyle']
        v_ = ['DCT_1st_DCT_2nd', x_list, y_list, 'blue', '--']
        line_dict_3 = dict(zip(k_, v_))

        x_list = sigma_list
        y_list = DCT_1st_BIOR_2nd_list
        k_ = ['name', 'x', 'y', 'color', 'linestyle']
        v_ = ['DCT_1st_BIOR_2nd', x_list, y_list, 'red', '--']
        line_dict_4 = dict(zip(k_, v_))

        plt = plot_dict_res(line_dict_1, line_dict_2, line_dict_3, line_dict_4, x_lable='sigma', y_label='PSNR',
                            im_label=im_name)
