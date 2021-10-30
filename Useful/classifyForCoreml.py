# 로컬에있는 데이터를 애플 createML에 학습하기 좋게 변환해서 저장하는 코드.

import sys
import numpy as np
import pandas as pd
from PIL import Image
sys.setrecursionlimit(100000)

tickers = ["BTC", "ETH","ADA", "XRP", "DOGE", "DOT"]
labels = pd.DataFrame()
images_len = []
for ticker in tickers:
    lable_path = f"/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/Model/data/({ticker})minut5_20c3s/labels.xlsx"
    labels_sub = pd.read_excel(lable_path)
    images_len.append(len(labels_sub))
    labels = pd.concat([labels, labels_sub])
labels = np.array(labels).reshape(-1,)
print("len(labels) : ",len(labels))
images = []
for ticker in tickers:
    ln = images_len.pop(0)
    print(ln)
    for i in range(ln):
        image_path = f"/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/Model/data/({ticker})minut5_20c3s/{i}.jpg"
        image = Image.open(image_path)
        image = Image.Image.resize(image,(128,64))
        images.append(image)
print("len(images) : ",len(images))

print(len(images))
index_a = 0
index_b = 0
for i in range(len(labels)):
    if labels[i] == 0:
        savePath = f"/Users/ubinyou/Desktop/codeML/Train/{labels[i]}/{index_a}.jpg"
        index_a += 1
    else:
        savePath = f"/Users/ubinyou/Desktop/codeML/Train/{labels[i]}/{index_b}.jpg"
        index_b += 1
    Image.Image.save(images[i], savePath)