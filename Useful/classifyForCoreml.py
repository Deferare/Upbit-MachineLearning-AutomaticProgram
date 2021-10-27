# 로컬에있는 데이터를 애플 createML에 학습하기 좋게 변환해서 저장하는 파일.

import sys
import numpy as np
import pandas as pd
from PIL import Image
sys.setrecursionlimit(100000)

lable_path = "/Model/data/minute_5_lable.xlsx"
labels = pd.read_excel(lable_path)
labels = np.array(labels[10000:]).reshape(-1,)
print(len(labels))
images = []
for i in range(10000, len(labels)+10000):
    image_path = f"/Model/data/minute_5/{i}.jpg"
    image = Image.open(image_path)
    images.append(image)

print(len(images))
index_a = 0
index_b = 0
for i in range(len(labels)):
    if labels[i] == 0:
        savePath = f"/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/data/CoreMLData/minute_5/Test/{labels[i]}/{index_a}.jpg"
        index_a += 1
    else:
        savePath = f"/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/data/CoreMLData/minute_5/Test/{labels[i]}/{index_b}.jpg"
        index_b += 1
    Image.Image.save(images[i], savePath)