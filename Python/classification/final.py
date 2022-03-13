import cv2
import joblib
import numpy as np
from image_tool import bgr_feature, hsv_feature, lab_feature
model = joblib.load('classify.model')
X = []
image = cv2.imread('2k_gd.bmp')
bgr_hist = bgr_feature(image)
hsv_hist = hsv_feature(image)
lab_hist = lab_feature(image)
feature = np.concatenate((hsv_hist, bgr_hist, lab_hist), axis=0) #按行拼接
feature = feature.T
X.append(feature)
X = np.squeeze(np.array(X), axis=1)
y_pred = model.predict(X)
print(y_pred)