import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import auc

from BM_influenced_by_denoising_methods.patch_matching import compute_patch_distance
from BM_influenced_by_denoising_methods.recall_precision import distance_2_precision_recall_fpRate


def compute_fpr_tpr(im, im_est, k):
    im_dist_table = compute_patch_distance(im, k)
    est_dist_table = compute_patch_distance(im_est, k)
    max_dist = np.max(im_dist_table)

    fp_rate_list = list()
    tp_rate_list = list()
    precision_list = list()
    recall_list = list()
    thre_list = list(np.arange(-1, 102) / 100 * max_dist)
    fixed_thr = max_dist / 2
    for thre in thre_list:
        pr, rc, fpr = distance_2_precision_recall_fpRate(im_dist_table, est_dist_table, fixed_thr, thre)
        fp_rate_list.append(fpr)
        tp_rate_list.append(rc)
        precision_list.append(pr)
        recall_list.append(rc)
    fp_rate_list.append(0)
    tp_rate_list.append(0)
    return fp_rate_list, tp_rate_list


def draw_ROC(fpr, tpr):
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, lw=1, alpha=0.7, label='AUC = %0.2f' % (roc_auc))
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('RoC Curve')
    plt.legend(loc="lower right")
    return plt


if __name__ == '__main__':
    import os
    import cv2
    from utils import add_gaussian_noise
    from plot_list_dict import plot_dict_res

    from denoising_method_NLM import nlm_denoise
    from denoising_method_TV import tv_denoise
    from denoising_method_Wavelet import wavelet_denoise

    save_dir = 'RoC_result/'
    os.makedirs(save_dir, exist_ok=True)

    patch_k = 9

    im_dir = 'special_test_image'

    sigma_list = [10, 20, 30, 40, 60, 80, 100]
    for im_name in os.listdir(im_dir):

        auc_list_noisy = list()
        auc_list_nlm = list()
        auc_list_tv = list()
        auc_list_Wavelet = list()
        for sigma in sigma_list:
            im_path = os.path.join(im_dir, im_name)
            im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
            noisy_im = add_gaussian_noise(im, sigma, seed=1)

            fpr_list, tpr_list = compute_fpr_tpr(im, noisy_im, patch_k)
            roc_auc = auc(fpr_list, tpr_list)
            # plt.plot(fpr_list, tpr_list, lw=1, alpha=0.7, color='black', linestyle='--',
            #          label='noisy_im_AUC=%0.6f' % (roc_auc))
            auc_list_noisy.append(roc_auc)

            im_est = nlm_denoise(noisy_im, sigma)
            fpr_list, tpr_list = compute_fpr_tpr(im, im_est, patch_k)
            roc_auc = auc(fpr_list, tpr_list)
            # plt.plot(fpr_list, tpr_list, lw=1, alpha=0.7, color='gold', linestyle='--',
            #          label='NLM_AUC=       %0.6f' % (roc_auc))
            auc_list_nlm.append(roc_auc)

            im_est = tv_denoise(noisy_im, sigma)
            fpr_list, tpr_list = compute_fpr_tpr(im, im_est, patch_k)
            roc_auc = auc(fpr_list, tpr_list)
            # plt.plot(fpr_list, tpr_list, lw=1, alpha=0.7, color='red', linestyle='--',
            #          label='TV_AUC=          %0.6f' % (roc_auc))
            auc_list_tv.append(roc_auc)

            im_est = wavelet_denoise(noisy_im)
            fpr_list, tpr_list = compute_fpr_tpr(im, im_est, patch_k)
            roc_auc = auc(fpr_list, tpr_list)
            # plt.plot(fpr_list, tpr_list, lw=1, alpha=0.7, color='blue', linestyle='--',
            #          label='Wavelet_AUC= %0.6f' % (roc_auc))
            auc_list_Wavelet.append(roc_auc)

            # plt.xlabel('False Positive Rate')
            # plt.ylabel('True Positive Rate')
            # plt.title(im_name + ' RoC Curve')
            # plt.legend(loc="lower right")
            #
            # plt.savefig(os.path.join(save_dir, im_name[:-4] + '+sigma-' + str(sigma)))
            # plt.close()

        k_ = ['name', 'x', 'y', 'color', 'linestyle']
        x_list = sigma_list
        y_list = auc_list_noisy
        v_ = ['auc_noisy', x_list, y_list, 'black', '--']
        line_dict = dict(zip(k_, v_))

        x_list = sigma_list
        y_list = auc_list_nlm
        v_ = ['auc_nlm', x_list, y_list, 'gold', '--']
        line_dict_2 = dict(zip(k_, v_))

        x_list = sigma_list
        y_list = auc_list_tv
        v_ = ['auc_tv', x_list, y_list, 'red', '--']
        line_dict_3 = dict(zip(k_, v_))

        x_list = sigma_list
        y_list = auc_list_Wavelet
        v_ = ['auc_Wavelet', x_list, y_list, 'blue', '--']
        line_dict_4 = dict(zip(k_, v_))

        pltt = plot_dict_res(line_dict, line_dict_2, line_dict_3, line_dict_4, im_label='AUC_'+im_name, x_lable='sigma', y_label='AUC')
        plt.savefig(os.path.join('AUC_result', im_name))
        plt.close()
