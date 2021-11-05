# Upbit-MachineLearning-AutomaticProgram
기본적으로 비트코인에 대한 예측을 지원합니다.</br>
학습 데이터는 비트코인, 이더리움, 리플, 에이다, 도지 코인, 폴카닷 총 6종료의 코인에 대해서 업비트 API를 활용하여 주가 데이터를 수집한 뒤,</br>
mplfinance로 약 5만 장가량의 커스터마이징 차트 이미지를 만들었습니다.</br>
이렇게 모아진 데이터에서 장대양봉이 연속 3번 등장할 경우와 장대음봉이 연속 3번 등장할 경우로 이진 분류가 가능한 학습 데이터로 필터링하여,</br>
5만 장 중 1.5만장 가량의 학습 데이터를 추출할 수 있었습니다.</br>
그리고 tensorflow의 CNN 모델로 학습을 시킨 후, 파이썬 비동기 처리와 업비트 API로 실시간 주가 데이터를 받아오면서 특정 기준을 정하여 자동매매까지 구현하였습니다.</br>
