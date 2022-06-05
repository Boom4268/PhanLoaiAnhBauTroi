import cv2 as cv
import numpy as np

BIN_SIZE = 16
MOMENT_SIZE = 9

# hàm trích xuất các đặc trưng
def color_moment(image):
    chanels = cv.split(image)
    features = []
    for chanel in chanels:
        chanel = chanel/256
        c_mean = round(np.mean(chanel), 6)
        c_std = round(np.std(chanel), 6)
        c_skew = np.mean(abs(chanel - chanel.mean())**3)
        c_thirMoment = round(c_skew**(1./3), 6)
        #features.extend([c_mean, c_std, c_thirMoment])
        features.extend([c_mean, c_std, c_thirMoment])
    return features

# hàm tính khoảng cách đặc trưng của hai bức ảnh
def distance_moment_color(features_of_image1, features_of_image2):
    dist = 0;
    for i in range(MOMENT_SIZE):
        dist += abs(features_of_image1[i] - (features_of_image2[i]))
    return round(dist, 6)

# hàm chuẩn hóa histogram (không dùng)
def normalized_color_histogram(image):
    w, h, chanel = image.shape[:3]
    #print(w, h, chanel)
    size = w * h
    features = []
    for c in range(chanel):
        hist = np.squeeze(cv.calcHist([image], [c], None, [BIN_SIZE], [0, 256]))
        hist = hist/size
        features.extend(hist)
    return features
