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

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
X = []
y = []
count = 0
with open("data3.csv", 'r') as f:
    lines = f.readlines()
    for line in lines:
        splited = line.split("\t")
        image_path = "C:/Users/86159/Desktop/datas6/" + splited[0]
       # print(image_path)
        label = splited[1]
        image = cv2.imread(image_path)
        # image_gblr = iaa.GaussianBlur(10 + iap.Uniform(0.1, 3.0))(images=image)
        image_flr = iaa.Fliplr(1.0)(images=image)
        image_fud = iaa.Flipud(1.0)(images=image)
        image_add = iaa.AddElementwise((-40, 40))(images=image)
        image_mblur = iaa.MedianBlur(k=(3, 3))(images=image)
        image_tr = iaa.Affine(translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)})(images=image)
        image_rot = iaa.Affine(rotate=(-45, 45))(images=image)
        image_shear = iaa.Affine(shear=(-16, 16))(images=image)

        for img in [image, image_flr, image_fud,image_add ,image_mblur,image_tr,image_rot,image_shear ]:
            bgr_hist = bgr_feature(img)
            hsv_hist = hsv_feature(img)
            lab_hist = lab_feature(img)
            feature = np.concatenate((hsv_hist, bgr_hist, lab_hist), axis=0) #按行拼接
            feature = feature.T
            X.append(feature)
            y.append(int(label))
        print(count)
        count += 1


X = np.squeeze(np.array(X), axis=1)
y = np.array(y)
print(X.shape, y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)


def svm_cross_validation(train_x, train_y):
    model = SVC(kernel='rbf', probability=True)
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10], 'gamma': [0.001, 0.0001]}
    grid_search = GridSearchCV(model, param_grid, n_jobs = 8, verbose=1)
    grid_search.fit(train_x, train_y)
   # print(grid_search.get_params(),grid_search.score())
    best_parameters = grid_search.best_estimator_.get_params()
    for para, val in list(best_parameters.items()):
        print(para, val)
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
    model.fit(train_x, train_y)
    return model



model = svm_cross_validation(X_train, y_train)
y_pred = model.predict(X_test)
result = accuracy_score(y_test, y_pred)
joblib.dump(model,'classify.model')
classify_model=joblib.load('classify.model')
print(result)

