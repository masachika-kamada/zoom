import time
from concurrent.futures import ThreadPoolExecutor


class Hoge:
    def __init__(self):
        self.run_flag = True

    def loop(self):
        while self.run_flag:
            print("loop", self.run_flag)
            time.sleep(1)


def time_exit():
    cnt = 0
    print("time_exit", hoge.run_flag)
    while hoge.run_flag:
        time.sleep(1)
        print("time_exit", hoge.run_flag)
        cnt += 1
        if cnt > 5:
            hoge.run_flag = False


print("start")
executor = ThreadPoolExecutor(max_workers=2)
hoge = Hoge()
executor.submit(hoge.loop)
executor.submit(time_exit)
executor.shutdown()
