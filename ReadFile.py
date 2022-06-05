import csv
import numpy as np
import cv2 as cv
from FeatureExtraction import *
import os

def write_to_file(fileName):
    file = open(fileName, 'w')
    fileWrite = csv.writer(file)
    path = 'data';
    dem = 0
    list_label = os.listdir(path)
    for label in list_label:
        list_image_of_label = os.listdir(os.path.join(path, label))
        for image_file in list_image_of_label:
            path_of_image = os.path.join(path, label, image_file)
            image = cv.imread(path_of_image)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            image = cv.resize(image, (255, 170))
            colorMM = color_moment(image)
            colorMM.insert(0, dem)
            dem = dem+1
            colorMM.extend([label, path_of_image])
            fileWrite.writerow(colorMM)
    file.close()

def read_data(fileName):
    file = open(fileName, 'r')
    fileRead = csv.reader(file)
    header = next(fileRead)
    data = []
    for r in fileRead:
        if len(r) > 0:
            features = np.array(r[1:10], dtype=float);
            data.append({'feature': features, 'label': r[10], 'path': r[11]})
    return data;

write_to_file('data.csv')
# data = read_data('data.csv')
# print(data[0])