import websockets, asyncio, json, pyupbit
import time, datetime
import numpy as np
import pandas as pd
import tensorflow.keras as keras
from collections import deque
from Useful.learnDataSave import getImage
from Useful.AutoSale import upbitSale

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

        # 처음 실행시 가장 최근의 코인 가격 데이터 10개로 초기화.
        df = pyupbit.get_ohlcv(ticker="KRW-BTC", interval="minute5", count=10)
        df = df.drop(columns=["volume", "value"])
        datas = deque(); times = deque(df.iloc[:,[]].index)
        for i in range(len(df)):
            _push = []
            for j in range(4):
                _push.append(df.iloc[i, j])
            datas.append(_push)

        start_time = time.time()
        open = datas[-1][-1]; hight = open; low = open

        # Core.
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            time_check = time.time()-start_time
            recive = data["tp"]
            # 5분마다 캔들 차트 1칸씩 업데이트 됨.
            if time_check >= 300:
                arr = [open, hight, low, recive]
                datas.append(arr)
                t = time.localtime()
                crnt_time = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min)
                times.append(crnt_time)
                print(f"{len(datas)}/{15} - {crnt_time} - {arr}")
                if len(datas) == 15: # 캔들 15개 모이면 예측.
                    df = pd.DataFrame(data=datas, index=times, columns=columns)
                    crnt_path = f"{crnt_time}.jpg"
                    image = np.array([getImage(df, image_excute_path+crnt_path)])
                    result = model.predict_on_batch(image)
                    upbitSale(result[0][0])
                    print("result : ", result, end="\n\n")
                    for _ in range(6): # 모델 실행 후 앞에 캔들 몇개 뺌. (그러면 5분x6개 = 30분 뒤에 다시 예측.)
                        datas.popleft()
                        times.popleft()

                # 초기화.
                start_time = time.time()
                open = 0; hight = 0; low = 2000000000
                continue

            # 실시간 BTC price 갱신.
            if open == 0:
                open = recive
            if recive > hight: hight = recive
            if recive < low: low = recive

async def main():
    await upbit_client()

asyncio.run(main())