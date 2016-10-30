import time

class Duration:
    def __init__(self,seconds):
        self.seconds = seconds
    def __repr__(self):
        return '{:0.8f} secs'.format(self.seconds)

class Timer:
    def __init__(self):
        self.duration = 0
    def start(self):
        self.start_time = time.perf_counter()
    def stop(self):
        self.stop_time = time.perf_counter()
        self.duration = Duration(self.stop_time - self.start_time)

if (__name__ == '__main__'):
    timer = Timer()
    timer.start()
    time.sleep(1)
    timer.stop()
    print(timer.duration)