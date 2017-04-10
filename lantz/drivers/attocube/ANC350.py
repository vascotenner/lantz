from lantz.foreign import LibraryDriver
from lantz import Feat, DictFeat, Action

import time
from ctypes import c_uint, c_void_p, c_double, pointer, POINTER

class ANC350(LibraryDriver):

    LIBRARY_NAME = 'anc350v3.dll'
    LIBRARY_PREFIX = 'ANC_'

    RETURN_STATUS = {0:'ANC_Ok', -1:'ANC_Error', 1:"ANC_Timeout", 2:"ANC_NotConnected", 3:"ANC_DriverError",
                     7:"ANC_DeviceLocked", 8:"ANC_Unknown", 9:"ANC_NoDevice", 10:"ANC_NoAxis",
                     11:"ANC_OutOfRange", 12:"ANC_NotAvailable"}

    def __init__(self):
        super(ANC350, self).__init__()

        ifaces = c_uint(0x01) # USB interface
        devices = c_uint()
        status = self.lib.discover(ifaces, pointer(devices))
        if not devices.value:
            raise RuntimeError('No controller found. Check if controller is connected or if another application is using the connection')
        print('discover status:', status)
        print('found devices:', devices.value)
        dev_no = c_uint(devices.value - 1)
        print('trying dev no:', dev_no.value)
        device = c_void_p()
        status = self.lib.connect(dev_no, pointer(device))
        print('connect status:', status)
        self.device = device

        time.sleep(0.5)


        self.lib.getFrequency.argtypes = [c_void_p, c_uint, POINTER(c_double)]
        self.lib.setFrequency.argtypes = [c_void_p, c_uint, c_double]
        self.lib.setDcVoltage.argtypes = [c_void_p, c_uint, c_double]
        self.lib.getPosition.argtypes = [c_void_p, c_uint, POINTER(c_double)]
        self.lib.measureCapacitance.argtypes = [c_void_p, c_uint, POINTER(c_double)]
        self.lib.startContinousMove.argtypes = [c_void_p, c_uint, c_uint, c_uint]
        self.lib.setTargetPosition.argtypes = [c_void_p, c_uint, c_double]



        return

    @DictFeat(units='Hz')
    def frequency(self, axis):
        ret_freq = c_double()
        err = self.lib.getFrequency(self.device, axis, pointer(ret_freq))
        return ret_freq.value

    @frequency.setter
    def frequency(self, axis, freq):
        err = self.lib.setFrequency(self.device, axis, freq)
        return err

    @DictFeat(units='um')
    def position(self, axis):
        ret_pos = c_double()
        self.lib.getPosition(self.device, axis, pointer(ret_pos))
        return ret_pos.value * 1e6

    @DictFeat(units='F')
    def capacitance(self, axis):
        ret_c = c_double()
        self.lib.measureCapacitance(self.device, axis, pointer(ret_c))
        return ret_c.value

    @DictFeat()
    def status(self, axis):
        status_names = [
            'connected',
            'enabled',
            'moving',
            'target',
            'eot_fwd',
            'eot_bwd',
            'error',
        ]
        status_flags = [c_uint() for _ in range(7)]
        status_flags_p = [pointer(flag) for flag in status_flags]
        self.lib.getAxisStatus(self.device, axis, *status_flags_p)

        ret = dict()
        for status_name, status_flag in zip(status_names, status_flags):
            ret[status_name] = True if status_flag.value else False
        return ret

    @Action()
    def jog(self, axis, speed):
        backward = 0 if speed >= 0.0 else 1
        start = 1 if speed != 0.0 else 0
        self.lib.startContinousMove(self.device, axis, start, backward)
        return

    @Action()
    def absolute_move(self, axis, target):
        self.lib.setTargetPosition(self.device, axis, target)
        enable = 0x01
        relative = 0x00
        self.lib.startAutoMove(self.device, axis, enable, relative)
        return

    @Action()
    def dc_bias(self, axis, voltage):
        err = self.lib.setDcVoltage(self.device, axis, voltage)
        return err


def main():
    import time
    import numpy as np
    anc = ANC350()
    # for axis in range(3):
    #     print(anc.frequency[axis])
    #     time.sleep(0.2)
    #     print(anc.position[axis])
    #     print(anc.capacitance[axis])
    # print(anc.position[0])
    # anc.jog(0, 1.0)
    # time.sleep(0.5)
    # anc.jog(0, 0.0)
    # print(anc.position[0])
    # anc.jog(0, -1.0)
    # time.sleep(0.5)
    # anc.jog(0, 0.0)
    print(anc.status[0])
    for pos in np.linspace(35e-6, 1000e-6, 20):
        anc.absolute_move(0, pos)
        print(anc.position[0])
        print(anc.status[0]['moving'])
        time.sleep(0.5)
    anc.absolute_move(0, 35e-6)
    while anc.status[0]['moving']:
        print('moving')

if __name__ == '__main__':
    main()
