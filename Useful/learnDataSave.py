import pyupbit, matplotlib
import pandas as pd
import numpy as np
import mplfinance as mpf
from PIL import Image
from Useful.Labeling import myLabeling
matplotlib.use("Agg")


# Chart save options.
rc = {
    "axes.labelcolor": "none",
    "axes.spines.bottom": False,
    "axes.spines.left": False,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.size": 0,
    "xtick.color": "none",
    "ytick.color": "none",
}
color_set = {"up":"#FF0000", "down":"#0F00FF"}
mc = mpf.make_marketcolors(up='#FF0000', down='#0F00FF',
                           edge=color_set, wick=color_set, alpha = 1.0,
                           volume="white")
style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc)
save = dict(dpi=150, transparent=True, bbox_inches='tight', facecolor="black")

# If one candle meets the condition,
# save the corresponding candle as a label and the chart of the preceding n candles in the corresponding candle as a feature image.
def learnDataSave(ticker,path_base, n): # path_base = Directory.
    df = pyupbit.get_ohlcv(ticker=ticker, interval="minute5", count=527385) # 4xx385 max.
    one = 0; zero = 0
    df.info()
    print()
    labeling_data = []
    name_i = 0
    i = n
    print(f"Start ----- {i}/{len(df)}")
    while i < len(df)-2:
        try:
            if i%1000 == 0:
                print(f"{i}_Ongoing - total : {name_i}    U1 : {one}    D1 : {zero}")
            label_result_1 = myLabeling(df["open"][i], df["high"][i], df["low"][i], df["close"][i])
            label_result_2 = myLabeling(df["open"][i+1], df["high"][i+1], df["low"][i+1], df["close"][i+1])
            label_result_3 = myLabeling(df["open"][i+2], df["high"][i+2], df["low"][i+2], df["close"][i+2])
            if label_result_1[0] == "U" and label_result_2[0] =="U" and label_result_3[0] =="U":
                label_value = 1
                one += 1
            elif label_result_1[0] == "D" and label_result_2[0] == "D" and label_result_3[0] =="D":
                label_value = 0
                zero += 1
            else:
                i += 1
                continue
            save["fname"] = path_base+f"{name_i}.jpg"
            # scale_width_adjustment = dict(volume=1.0, candle=1.0)
            mpf.plot(df[i-n:i], type='candle', style=style_final, figsize=(2.56, 1.28), savefig=save, volume=True)
            labeling_data.append(label_value)
            name_i += 1
            i += 1
        except:
            print(f"- Error : Ended unexpectedly and saved up to {name_i}.")
            pd.DataFrame(labeling_data).to_excel(path_base + "labels.xlsx", index=False)
            exit(0)

    pd.DataFrame(labeling_data).to_excel(path_base+"labels.xlsx", index=False)
    print(f"Completion - total : {name_i}    U1 : {one}    D1 : {zero}")

# dataFrame -> Image save and the return
def getImage(datas, image_path):
    save["fname"] = image_path
    mpf.plot(datas, type='candle', style=style_final, figsize=(2.56, 1.28), savefig=save, volume=True)
    image = Image.open(image_path)
    image = Image.Image.resize(image, (128, 64))
    return np.array(image) / 255

# -------------------------------- Excution phrase.

# tickers = ["KRW-BTC", "KRW-ETH","KRW-ADA", "KRW-XRP", "KRW-DOGE", "KRW-DOT"]
# for ticker in tickers:
#     t = ticker[4:]
#     path = f"/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/Model/data/({t})minut5_20c3s/"
#     learnDataSave(ticker, path, 20)
