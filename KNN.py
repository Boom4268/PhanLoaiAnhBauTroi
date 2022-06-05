import numpy as np
from ReadFile import *
from FeatureExtraction import *
import cv2 as cv

# thuật toán KNN
def KNN(data, pointA, k=1):
    #tính khoảng cách
    list = []
    for point in data:
        dist = distance_moment_color(point['feature'], pointA)
        list.append({'dist': dist, 'label': point['label'], 'path': point['path']})#
    list.sort(key=lambda x: x['dist'])
    return list[:k]

# phân loại nhãn: nhãn có số lượng cao nhất trong k bức ảnh sẽ lấy để làm nhãn
def mostLabel(list):
    res = ''
    rate = 0
    labels = []
    for l in list:
        labels.append(l['label'])
    for label in labels:
        if(labels.count(label) > rate):
            res = label
            rate = labels.count(label)
    return res
