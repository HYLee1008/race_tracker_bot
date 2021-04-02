Race Tracker Bot
==================
자 드가자~

Note
---------
 - 현재 1loop에 4초 소요. 더 줄이는 방법 찾아보기.
 - async를 사용하면 4.5초 소요. 공식 API에서 async를 사용하기 때문으로 추정.
 - Thread를 사용하면 0.7초 소요. VM에서는 2배 시간 소요. 하지만 전역변수 공유 문제 발생 가능성 농후

History
---------
- 2021-03-27 : Version 2 생성. 비공식 API를 사용하여 속도 향상. Thread 사용.
- 2021-03-30 : Out of memory로 인해 VM 멈춤 현상 발견. WinError 10048 발생. 너무 자주 request를 보내서 생기는 오류인것 같다.
- 2021-04-01 : sleep을 사용해도 같은 error 발생. url을 읽을 때, poolManager를 이용해 문제해결
- 2021-04-02 : 여전히 같은 error 발생. async로 다시 시도해봄. 

Description
----------
rtb version 2.