import numpy as np


def distance_2_precision_recall_fpRate(original_im_distance, noisy_im_distance, fixed_threshold, threshold):
    ground_truth = original_im_2_ground_truth(original_im_distance, fixed_threshold)
    predict = noisy_im_2_predict(noisy_im_distance, threshold)
    precision, recall, fp_rate = calculate_precision_recall(ground_truth, predict)
    return precision, recall, fp_rate


def original_im_2_ground_truth(ori_im_distance, threshold):
    ground_truth = np.where(ori_im_distance > threshold, 1, 0)
    return ground_truth


def noisy_im_2_predict(noisy_im_distance, threshold):
    predict = np.where(noisy_im_distance > threshold, 1, 0)
    return predict


def calculate_precision_recall(ground_truth, predict):
    """
    :param ground_truth:  bin (0:false, 1: True)
    :param predict: bin (0:false, 1: True)
    :return:
    """
    tp = np.sum(np.logical_and(ground_truth, predict))
    fn = np.sum(np.logical_and(ground_truth, 1 - predict))
    fp = np.sum(np.logical_and(1 - ground_truth, predict))
    tn = np.sum(np.logical_and(1 - ground_truth, 1 - predict))

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    fp_rate = fp / (fp + tn)

    return precision, recall, fp_rate


if __name__ == '__main__':
    gt = np.array([1, 1, 0, 0, 1])
    pre = np.array([1, 0, 1, 1, 1])

    precision, recall, fp_rate = calculate_precision_recall(gt, pre)
    print(precision)
    print(recall)
