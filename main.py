import time
import websockets
import asyncio
import json
import matplotlib
import mplfinance as mpf
import numpy as np
matplotlib.use("Agg")

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
image_save_path = "/Users/ubinyou/Documents/Task/Upbit-MachineLearning-AutomaticProgram/data/"

# 차트 저장 옵션.
mc = mpf.make_marketcolors(up='red', down='blue', inherit=True)
style_final = mpf.make_mpf_style(marketcolors=mc, rc=rc)
save = dict(dpi=100, transparent=True, bbox_inches='tight', facecolor="black")



async def upbit_client():
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri) as websocket:
        subscribe_fmt = [
            {"ticket":"Trade"},
            {
                "type": "ticker",
                "codes":["KRW-BTC", "KRW-XRP", "KRW-ETH"],
                "isOnlyRealtime": True
            },
            {"format":"SIMPLE"}
        ]
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        datas = []
        start_time = time.time()
        open = 0; hight = 0; low = 1000000000
        while True:
            data = await websocket.recv()
            data = json.loads(data)

            time_check = time.time()-start_time
            # 5분마다 실행.
            if time_check >= 300:
                datas.append([open, hight, low, data["tp"]])
                print("DB save.")
                print(time_check)
                print()
                # 시간, 가격 초기화.
                start_time = time.time()
                open = 0;hight = 0;low = 1000000000
                if len(datas) == 15:
                    pass
                continue


            if data["cd"] == "KRW-BTC":
                recive = int(data["tp"])
                if open == 0:
                    open = recive
                if recive > hight: hight = recive
                if recive < low: low = recive
                print(f"open : {open}  hight : {hight}  low : {low}")
async def main():
    await upbit_client()
asyncio.run(main())