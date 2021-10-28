# 그냥 테스트 하는곳.

import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
import sys, os, pyupbit


# n = 60
# seed = 5
# images = []
# for i in range(seed,n+seed):
#     image_path = f"/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/Model/data/minute_5/{i}.jpg"
#     image = Image.open(image_path)
#     image = Image.Image.resize(image,(256,138))
#     images.append(np.array(image)/255)
# # plt.imshow(images[n-1])
# # plt.show()
#
# images = np.array(images)
#
# model_path = "/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/Model/minute5/2/minute5.h5"
# model = keras.models.load_model(model_path)
#
#
# cnt_1 = 0
# cnt_2 = 0
# predicts = model.predict(images[:])
# for result in predicts:
#     if result[0] >= 0.75:
#         cnt_1 += 1
#     elif result[0] <= 0.15:
#         cnt_2 += 1
#     print(result[0])
# print()
# print("len : ", len(predicts))
# print(cnt_1)
# print(cnt_2)
import time, datetime

df = pyupbit.get_ohlcv(ticker="KRW-BTC", interval="minute5", count=10)
df = df.drop(columns=["volume", "value"])
arr = []
times = list(df.iloc[:,[]].index)
for i in range(len(df)):
    _push = []
    for j in range(4):
        _push.append(df.iloc[i,j])
    arr.append(_push)

print()
print(df)
print(len(arr))
print(arr)
print()
print(len(times))
print(times)