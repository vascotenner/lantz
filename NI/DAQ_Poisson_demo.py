#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lantz.drivers.ni.daqmx import CounterOutputTask, CounterOutTicksChannel
from lantz.drivers.ni.daqmx import CounterInputTask, CountEdgesChannel

poisson = CounterOutputTask('poisson')
poiss_chan2 = CounterOutTicksChannel('dev1/ctr1')
poisson.add_channel(poiss_chan2)


counts = CounterInputTask('counter')
chan1 = CountEdgesChannel('dev1/ctr0')
counts.add_channel(chan1)
counts.start()

print('Counts:{}'.format(counts.read(samples_per_channel=1)))

counts.stop()
