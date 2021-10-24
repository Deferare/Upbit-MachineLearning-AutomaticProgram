import pandas as pd
import pyupbit
import mplfinance as mpf
import matplotlib
from Useful.Labeling import myLabeling
matplotlib.use("Agg")

# api 관련.
ACCESS_KEY = "AAPWbiqKibiFVREqoTfy0wj3WgTPVK4otjub7QLo"
SECRET_KEY = "oqXYFxvflQhoHThaeQNhuFSpegVxPjQxceh5Ep7r"

# data save 관련.
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

# 차트 저장 옵션.
mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc)
save = dict(dpi=100, transparent=True, bbox_inches='tight', facecolor="black")

df = pyupbit.get_ohlcv(ticker="KRW-BTC", interval="minute5", count=427385)
print(df.info())

path_base = "/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/data/minute_5/"
labeling_data = []
name_i = 0
i = 15
while i < len(df):
    try:
        if i%5000 == 0:
            print(i)
        label_result = myLabeling(df["open"][i], df["high"][i], df["low"][i], df["close"][i])
        if label_result[0] == "U":
            save["fname"] = path_base+f"{name_i}.jpg"
            mpf.plot(df[i-15:i], type='candle', style=style_final, figsize=(3, 1.5), savefig=save)
            labeling_data.append(1)
            name_i += 1
            i += 15
        elif label_result[0] == "D":
            save["fname"] = path_base+f"{name_i}.jpg"
            mpf.plot(df[i-15:i], type='candle', style=style_final, figsize=(3, 1.5), savefig=save)
            labeling_data.append(0)
            name_i += 1
            i += 15
        else:
            i += 1
    except:
        pd.DataFrame(labeling_data).to_excel(path_base + "labels.xlsx", index=False)

pd.DataFrame(labeling_data).to_excel(path_base+"labels.xlsx", index=False)

