import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from numpy import arange
from numpy.random import rand

from lantz.drivers.ni.daqmx import AnalogInputTask, Task, DigitalInputTask
from lantz.drivers.ni.daqmx import VoltageInputChannel
task = AnalogInputTask('test')
task.add_channel(VoltageInputChannel('dev1/ai0'))
task.add_channel(VoltageInputChannel('dev1/ai1'))
task.start()

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
t0 = time.clock()
xar = []
yar0 = []
yar1 = []

def animate(i):
    xar.append(time.clock()-t0)
    vals = task.read(samples_per_channel=1, timeout=10.0, group_by='scan')
    yar0.append(vals[0][0])
    yar1.append(vals[0][1])
    ax1.clear()
    ax1.plot(xar, yar0, 'bo')
    ax1.plot(xar, yar1, 'ro')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
ani = animation.FuncAnimation(fig, animate, interval=10)

plt.show()

task.stop()
