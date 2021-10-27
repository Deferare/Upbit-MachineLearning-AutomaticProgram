import websockets, asyncio, json
import time, datetime
import mplfinance as mpf
import numpy as np
import pandas as pd
import tensorflow.keras as keras
from collections import deque
from Useful.learnDataSave import getImage
from Useful.AutoSale import upbitSale

# 차트 저장 옵션.
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
mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc)
save = dict(dpi=100, transparent=True, bbox_inches='tight', facecolor="black")

image_excute_path = "/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/Model/data/execute/" # 실시간 예측 차트 담길 폴더.
model_path = "/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/Model/minute5/2/minute5.h5" # 사용 할 모델.

async def upbit_client():
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri) as websocket:
        subscribe_fmt = [
            {"ticket":"Trade"},
            {
                "type": "ticker",
                "codes":["KRW-BTC"],
                "isOnlyRealtime": True
            },
            {"format":"SIMPLE"}
        ]
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)
        model = keras.models.load_model(model_path)
        columns = ["open", "high", "low", "close"]
        datas = deque(); times = deque()
        start_time = time.time()
        open = 0; hight = 0; low = 1000000000

        # Core.
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            time_check = time.time()-start_time

            # 5분마다 캔들 차트 1칸씩 업데이트 됨.
            if time_check >= 300:
                datas.append([open, hight, low, data["tp"]])
                t = time.localtime()
                crnt_time = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min)
                times.append(crnt_time)
                print(crnt_time)
                if len(datas) == 15: # 캔들 15개 모이면.
                    df = pd.DataFrame(data=datas, index=times, columns=columns)
                    crnt_path = f"{crnt_time}.jpg"
                    image = np.array([getImage(df, image_excute_path+crnt_path)])
                    result = model.predict_on_batch(image)
                    upbitSale(result[0][0])
                    print("result : ", result, end="\n\n")
                    for _ in range(6): # 앞에 6개 뺌. (그러면 5분x6 = 30분 뒤에 다시 예측 됨)
                        datas.popleft()
                        times.popleft()

                # 초기화.
                start_time = time.time()
                open = 0;hight = 0;low = 1000000000
                continue

            # BTC price 갱신.
            recive = data["tp"]
            if open == 0:
                open = recive
            if recive > hight: hight = recive
            if recive < low: low = recive

async def main():
    await upbit_client()

asyncio.run(main())



