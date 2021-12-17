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


n = 96
seed = 0
images = []
for i in range(seed,n+seed):
    image_path = f"/Users/deforeturn/Github/Upbit-MachineLearning-AutomaticProgram/Model/data/(BTC)minut5_20c3s/{i}.jpg"
    image = Image.open(image_path)
    image = Image.Image.resize(image,(128,64))
    images.append(np.array(image)/255)

images = np.array(images)
#
model_path = "/Users/deforeturn/Github/Upbit-MachineLearning-AutomaticProgram/Model/minut5_20c3s/3/myModel.h5"
model = keras.models.load_model(model_path)


cnt_1 = 0
cnt_2 = 0
predicts = model.predict(images[:])
for result in predicts:
    if result[1] >= 0.8 and result[0] <= 0.3:
        cnt_1 += 1
    elif result[0] >= 0.7 and result[1] <= 0.3:
        cnt_2 += 1
    print(result)
print()
print("len : ", len(predicts))
print(cnt_1)
print(cnt_2)