
# 장대 양봉이면 U1, 장대 음봉이면 D1, 그 외 -1 반환.
def myLabeling(S, H, L, E): # 시가 고가 저가 종가.
    up_down_state = E - S
    if up_down_state > 0:
        body = E - S
        top_t = H - E
        bottom_t = S - L
    else:
        body = S - E
        top_t = H - S
        bottom_t = E - L
    candle_sum = top_t + bottom_t + body

    if candle_sum == 0:
        candle_sum = 1

    body = round(body / candle_sum, 5)

    if up_down_state > 0:
        answer = "U"
    else:
        answer = "D"
    if body >= 1:
        answer += '1'
    else:
        answer = "-1"
    return answer