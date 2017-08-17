import ctypes
import time
from io import BytesIO
import struct

from lantz.foreign import LibraryDriver
from lantz import Feat, DictFeat, Action

TTREADMAX = 131072
FIFOFULL = 0x0003

class PH300(LibraryDriver):

    LIBRARY_NAME = 'phlib64.dll'
    LIBRARY_PREFIX = 'PH_'

    def __init__(self, device_idx):
        super().__init__()
        self.device_idx = device_idx
        return

    def initialize(self):
        serial = ctypes.create_string_buffer(8)
        self.lib.OpenDevice(self.device_idx, serial)
        self.lib.Initialize(self.device_idx, 2)
        features = ctypes.c_int()
        self.lib.GetFeatures(self.device_idx, ctypes.byref(features))
        return

    @DictFeat(keys=(0, 1))
    def count_rate(self, channel):
        rate = ctypes.c_int()
        self.lib.GetCountRate(self.device_idx, channel, ctypes.byref(rate))
        return rate.value

    @Feat()
    def resolution(self):
        resolution = ctypes.c_double(0.0)
        self.lib.GetResolution(self.device_idx, ctypes.byref(resolution))
        return resolution.value

    @Action()
    def set_input_cfd(self, channel, level, zero_cross):
        self.lib.SetInputCFD(self.device_idx, channel, level, zero_cross)
        return

    @Action()
    def set_sync_div(self, sync_div):
        self.lib.SetSyncDiv(self.device_idx, sync_div)
        return

    @Action()
    def set_binning(self, binning):
        self.lib.SetBinning(self.device_idx, binning)
        return

    @Action()
    def set_offset(self, offset):
        self.lib.SetOffset(self.device_idx, offset)
        return

    @Action(units=('ms'))
    def start_measurement(self, measurement_time):
        self.lib.StartMeas(self.device_idx, int(measurement_time))
        return

    @Action()
    def stop_measurement(self):
        self.lib.StopMeas(self.device_idx)
        return

    @Feat()
    def elapsed_measurement_time(self):
        elapsed = ctypes.c_double(0.0)
        self.lib.GetElapsedMeasTime(self.device_idx, ctypes.byref(elapsed))
        return elapsed.value

    @Feat()
    def flags(self):
        flags = ctypes.c_uint()
        self.lib.GetFlags(self.device_idx, ctypes.byref(flags))
        return flags.value

    @Action()
    def read_fifo(self, nvalues=TTREADMAX):
        databuf = BytesIO()
        buf = (ctypes.c_uint * nvalues)()
        n_to_read = ctypes.c_uint(nvalues)
        n_read = ctypes.c_uint(0)
        while 1:
            if self.flags & FIFOFULL:
                break
            retcode = self.lib.ReadFiFo(self.device_idx, ctypes.byref(buf), n_to_read, ctypes.byref(n_read))
            if retcode < 0:
                break
            if n_read.value:
                databuf.write(bytes(buf)[:n_read.value * 4])
            else:
                break
        return databuf

    def gen_raw_tttr(self):
        buf = (ctypes.c_uint * nvalues)()
        n_to_read = ctypes.c_uint(TTREADMAX)
        n_read = ctypes.c_uint(0)
        while 1:
            if self.flags & FIFOFULL:
                break
            retcode = self.lib.ReadFiFo(self.device_idx, ctypes.byref(buf), n_to_read, ctypes.byref(n_read))
            if retcode < 0:
                break
            if n_read.value:
                yield bytes(buf)[:n_read.value * 4]
            else:
                break
        return

    def finalize(self):
        self.lib.CloseDevice(self.device_idx)
        return

def test():
    ph = PH300(0)
    ph.initialize()
    ph.set_sync_div(1)
    ph.set_input_cfd(0, 50, 10)
    ph.set_input_cfd(1, 50, 10)
    ph.set_binning(0)
    ph.set_offset(0)

    print(ph.count_rate[0], ph.count_rate[1])

    ph.start_measurement(1000)
    buf = ph.read_fifo(TTREADMAX)
    ph.stop_measurement()
    fifo_reader(buf)
    print(ph.count_rate[0], ph.count_rate[1])
    return

def fifo_reader(buf, resolution=4.0):
    buf.seek(0)
    t2_wraparound = 210698240

    counts = [0, 0]
    ofl_time = 0
    while 1:
        chunk = buf.read(4)
        if not chunk:
            break
        chunk = struct.unpack('<I', chunk)[0]

        time = chunk & 0x0FFFFFFF
        channel = (chunk & 0xF0000000) >> 28
        if channel == 0xF:
            # special record
            markers = time & 0xF
            if not markers:
                # overflow encountered
                ofl_time += t2_wraparound
            else:
                # marker encountered
                truetime = ofl_time + time
        else:

            if channel > 4:
                raise RuntimeError("illegal channel encountered")
            else:
                counts[(channel >= 1)] += 1
                truetime = (ofl_time + time) / 1e9 * resolution
                # print('{}\t{}\t{}'.format(truetime, *counts))
