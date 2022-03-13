import cv2
import joblib
import numpy as np
import glob
from Demo1 import myaug, lab_feature,bgr_feature,hsv_feature



model=joblib.load('classify.model')
X = []
img_path='1k_gd.bmp'
image = cv2.imread(img_path)
image = myaug(image, repeat=0)[0]
bgr_hist = bgr_feature(image)
hsv_hist = hsv_feature(image)
lab_hist = lab_feature(image)
feature = np.concatenate((hsv_hist, bgr_hist, lab_hist), axis=0) #按行拼接
feature = feature.T
X.append(feature)
X = np.squeeze(np.array(X), axis=1)
y_pred = model.predict(X)
print(img_path, y_pred)