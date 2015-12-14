import matplotlib.pyplot as plt
import time
import random
from collections import deque
import numpy as np

from lantz.drivers.ni.daqmx import AnalogInputTask, Task, DigitalInputTask
from lantz.drivers.ni.daqmx import VoltageInputChannel
# simulates input from serial port
def next_V_pt(task):
    while True:
        val = task.read_scalar()
        yield val


task = AnalogInputTask('test')
task.add_channel(VoltageInputChannel('dev1/ai0'))
task.start()

a1 = deque([0]*1000)
ax = plt.axes(xlim=(0, 1000), ylim=(-1, 1))
d = next_V_pt(task)

line, = plt.plot(a1)
plt.ion()
plt.ylim([-1, 1])
plt.show()

task.stop()

for i in range(0, 1000):
    a1.appendleft(next(d))
    datatoplot = a1.pop()
    line.set_ydata(a1)
    plt.draw()
    i += 1
    time.sleep(0.1)
    plt.pause(0.0001)
