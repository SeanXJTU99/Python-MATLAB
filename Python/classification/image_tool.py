import cv2
import datetime
import numpy as np
import matplotlib.pyplot as plt


def hsv_feature(img):
#    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)                    #图片rgb转hsv 返回hsv图像
    hist = cv2.calcHist([hsv], [0], None, [256], [0,255])
    return hist


def bgr_feature(img):
    # img = cv2.imread(image_path)
    hist = cv2.calcHist([img], [0], None, [256], [0.0, 255.0])
    return hist


def lab_feature(img):
    print(img.shape)
    # img = cv2.imread(image_path)
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    hist = cv2.calcHist([img_lab], [0], None, [256], [0, 255])
    return hist



if __name__ == '__main__':
    image_path = r"C:\Users\86159\Desktop\datas6\huali\cuguang\1.bmp"
    image = cv2.imread(image_path)
    print(image.shape)
    print(bgr_feature(image).shape)
    print(lab_feature(image).shape)
    print(hsv_feature(image).shape)