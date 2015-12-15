import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from numpy import arange
from numpy.random import rand

from lantz.drivers.ni.daqmx import AnalogInputTask, Task, DigitalInputTask
from lantz.drivers.ni.daqmx import VoltageInputChannel
task = AnalogInputTask('test')
task.add_channel(VoltageInputChannel('dev1/ai0'))
task.start()

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
t0 = time.clock()
xar = []
yar = []

def animate(i):
    xar.append(time.clock()-t0)
    yar.append(task.read_scalar())
    ax1.clear()
    ax1.plot(xar, yar, 'o')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
ani = animation.FuncAnimation(fig, animate, interval=10)

plt.show()

task.stop()
