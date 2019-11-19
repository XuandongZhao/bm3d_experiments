# bm3d_experiment


add unbiased estimation to the threshold

special_test_image contains the test images (images are not normal)  
RoC_result contains the RoC result  
AUC_result contains AUC under different sigma  

a fixed threshold(max_dist between patches / 2) is used to determine the ground truth   
a changing threshold(thre_list = list(np.arange(-1, 102) / 100 * max_dist)) is used to draw RoC curve  

