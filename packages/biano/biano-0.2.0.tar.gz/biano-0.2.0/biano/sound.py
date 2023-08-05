#coding=utf-8

import pyaudio
import numpy as np
import math
fps = 4096*10
p = pyaudio.PyAudio()
nbyte = 2
ndtype = np.int16
nmax = (1<<(nbyte<<3))-1

nrange = nmax/2
nrange = (nmax+1)/2
def fn(n):
    return 27.5*(2**(1/12))**(n-1)

pass

mid = 50
import random
def f(rate, n, sec = 1.0):
    global fps
    size = int(fps * sec)
    prev = 0*int(size*0.02)
    data = np.zeros(prev+size+int(size+0.5), dtype = ndtype)
    for i in range(size):
        x0 = i*2*math.pi*rate/fps
        #x0 += (random.random()-0.5)*0.1
        #sound = math.cos(abs(mid-n)/50*math.pi*0.5)
        # 50的音亮最大，再往左或往右的音量都调小
        sound = 1-abs(mid-n)/50
        if n > mid:
            sound = -sound
        y = math.sin(x0)*(0.7+sound*0.3)
        #y *=(1+(random.random()-0.5)*0.1)
        r = (size-i)/size
        y *= r
        #y *= math.cos(i*math.pi/size)*0.5+0.5
        y *= nrange
        y = max(-nrange,min(nrange-1, y))
        data[prev+i] = y
    return data#rst

pass

class CacheFc:
    def __init__(self):
        self.cache = {}
    def __call__(self, rate, n):
        if rate not in self.cache:
            self.cache[rate] = f(rate, n, 1.0)
        return self.cache[rate]

pass
def create():
    return p.open(format=p.get_format_from_width(nbyte), channels=1, rate=fps, output=True)

pass

def close(stream):
    stream.stop_stream()
    stream.close()

pass
import threading


class Sound:
    def run_zero(self):
        global fps
        size = int(fps)
        data = np.zeros(size, dtype = ndtype)
        while self.running:
            self.zero.write(data)
        close(self.zero)
    def __init__(self):
        self.fc = CacheFc()
        self.frees = [create() for i in range(20)]
        self.zero = create() #一直播放着空旋律，避免噪音
        self.index = 0
        self.lock = threading.Lock()
        self.running = True
        th = threading.Thread(target = self.run_zero)
        th.setDaemon(True)
        th.start()
    def _play(self, data, id):
        self.frees[id].write(data)
    def play(self, n):
        if not self.running:
            return
        rate = fn(n)
        data = self.fc(rate, n)
        with self.lock:
            id = self.index
            self.index = (self.index+1)%20
        th = threading.Thread(target = self._play, args =(data, id))
        th.setDaemon(True)
        th.start()
    def close(self):
        import time
        time.sleep(1.0)
        for st in self.frees:
            close(st)
        self.running = False

pass
sd = Sound()
def release():
    p.terminate()

pass
