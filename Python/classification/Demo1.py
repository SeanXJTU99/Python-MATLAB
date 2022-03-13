import cv2
import os

import numpy as np
from sklearn.svm import SVC
from image_tool import bgr_feature, hsv_feature, lab_feature
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import imgaug.augmenters as iaa
import joblib
from imgaug import parameters as iap


def _myaug(hsv_point=[100, 100, 100], delta=0.05):
    aug_hsv = [hsv_point[0],
               np.clip(hsv_point[1] + int(delta*255*(-1+2*np.random.rand())), 0, 255),
               np.clip(hsv_point[2] + int(delta*255*(-1+2*np.random.rand())), 0, 255)]
    return aug_hsv


def myaug(image, repeat=5, delta=0.05):
    hsv = cv2.cvtColor(np.uint8(image), cv2.COLOR_BGR2HSV)
    a, b, c = hsv[0][0], hsv[0][hsv.shape[1]//2], hsv[0][-1]
    abc = np.asarray([a,b,c]).reshape(1, -1, 3)
    aug_images = [abc]
    for i in range(repeat):
        a1, b1, c1 = _myaug(a, delta), _myaug(b, delta), _myaug(c, delta)
        tmp_img = np.asarray([a1, b1, c1]).reshape(1, -1, 3)
        aug_images.append(tmp_img)
    aug_images = [cv2.cvtColor(np.uint8(tmp_img), cv2.COLOR_HSV2BGR) for tmp_img in aug_images]
    return aug_images


os.environ["CUDA_VISIBLE_DEVICES"] = "0"
X = []
y = []
count = 0
with open("data16.csv", 'r') as f:
    lines = f.readlines()
    for line in lines:
        splited = line.split("\t")
        image_path = "C:/Users/86159/Desktop/data16/" + splited[0]
        # print(image_path)
        label = splited[1]
        image = cv2.imread(image_path)
        # image_gblr = iaa.GaussianBlur(10 + iap.Uniform(0.1, 3.0))(images=image)
        # image_flr = iaa.Fliplr(1.0)(images=image)
        # image_fud = iaa.Flipud(1.0)(images=image)
        # image_add = iaa.AddElementwise((-40, 40))(images=image)
        # image_mblur = iaa.MedianBlur(k=(3, 3))(images=image)
        # image_tr = iaa.Affine(translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)})(images=image)
        # image_rot = iaa.Affine(rotate=(-45, 45))(images=image)
        # image_shear = iaa.Affine(shear=(-16, 16))(images=image)
        aug_images = myaug(image)

        for img in aug_images:
            bgr_hist = bgr_feature(img)
            hsv_hist = hsv_feature(img)
            lab_hist = lab_feature(img)
            feature = np.concatenate((hsv_hist, bgr_hist, lab_hist), axis=0) #按行拼接
            # feature = bgr_hist
            feature = feature.T
            X.append(feature)
            y.append(int(label))
        # print(count)
        count += 1

from collections import Counter
print(Counter(y))

X = np.squeeze(np.array(X), axis=1)
y = np.array(y)
# (X.shape, y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)


def svm_cross_validation(train_x, train_y):
    model = SVC(kernel='rbf', probability=False)
   #  param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10], 'gamma': [0.001, 0.0001]}
   #  grid_search = GridSearchCV(model, param_grid, n_jobs = 8, verbose=1)
   #  grid_search.fit(train_x, train_y)
   # # print(grid_search.get_params(),grid_search.score())
   #  best_parameters = grid_search.best_estimator_.get_params()
   #  # for para, val in list(best_parameters.items()):
   #  #     print(para, val)
   #  model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=False)
    model.fit(train_x, train_y)
    return model



model = svm_cross_validation(X_train, y_train)
y_pred = model.predict(X_test)
result = accuracy_score(y_test, y_pred)
joblib.dump(model,'classify.model')
classify_model=joblib.load('classify.model')
print(result)

import glob
# 指定路径
img_list = r'C:/Users/86159/Desktop/svmceshi'
# 返回指定路径的文件夹名称
dirs = os.listdir(img_list)

for dir in dirs:
    # 拼接字符串
    pa = img_list +'/'+ dir
    print(pa)

    X = []
    image = cv2.imread(pa)
    image = myaug(image, repeat=0)[0]

    bgr_hist = bgr_feature(image)
    hsv_hist = hsv_feature(image)
    lab_hist = lab_feature(image)
    feature = np.concatenate((hsv_hist, bgr_hist, lab_hist), axis=0)  # 按行拼接
    feature = feature.T
    X.append(feature)
    X = np.squeeze(np.array(X), axis=1)
    y_pred = model.predict(X)
    print(pa, y_pred)
