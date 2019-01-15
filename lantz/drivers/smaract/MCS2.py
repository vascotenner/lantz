# -*- coding: utf-8 -*-
"""
    lantz.drivers.smaract.smaract.MCS2 axis
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    General class that implements the commands used for several smaract motion
    drivers using MCS2 dll

    :copyright: 2018, see AUTHORS for more details.
    :license: GPL, see LICENSE for more details.

    Source: Instruction Manual (Smaract)

"""

import ctypes as ct
from ctypes import byref

import lantz.drivers.smaract.SmarActControlConstants as SmarActControlConstants
from lantz.action import Action
from lantz.drivers.motion import MotionAxisMultiple, MotionControllerMultiAxis
from lantz.errors import InstrumentError
from lantz.feat import Feat
from lantz.foreign import LibraryDriver


def gen_dict_from_prefix(namespace, prefix):
    return {getattr(namespace, constant): constant[len(prefix):]
     for constant in dir(namespace)
     if constant.startswith(prefix)}


def invert_dict(d):
    return {val: key for key,val in d.items() }


# Generate dict of error codes from altered header file
_ERRORS = gen_dict_from_prefix(SmarActControlConstants, 'SA_CTL_ERROR_')

_MOVE_MODES =  gen_dict_from_prefix(SmarActControlConstants, 'SA_CTL_MOVE_MODE_')

_STATES = gen_dict_from_prefix(SmarActControlConstants, 'SA_CTL_CH_STATE_BIT_')

# List of functions that should not be checked for errorcodes
_IGNORE_ERR = []

SA_CTL_DeviceHandle_t = ct.c_uint32
SA_CTL_TransmitHandle_t = ct.c_uint32
SA_CTL_StreamHandle_t = ct.c_uint32

SA_CTL_RequestID_t = ct.c_uint8
SA_CTL_PropertyKey_t = ct.c_uint32
SA_CTL_Result_t = ct.c_uint32
size_t = ct.c_size_t
idx = ct.c_int8


class MCS2_Find_devices(LibraryDriver):
    """ Driver for MCS controller

    """
    LIBRARY_NAME = 'smaractctl'

    def _add_types(self):
        self.lib.SA_CTL_FindDevices.argtypes = [ct.c_char_p, ct.c_char_p, ct.POINTER(ct.c_size_t)]
        self.lib.SA_CTL_Open.argtypes = [ct.POINTER(SA_CTL_DeviceHandle_t), ct.c_char_p, ct.c_char_p]
        self.lib.SA_CTL_Move.argtypes = [SA_CTL_DeviceHandle_t, ct.c_int8, ct.c_int64, SA_CTL_TransmitHandle_t]

        self.lib.SA_CTL_GetProperty_i64.argtypes = [SA_CTL_DeviceHandle_t, idx, SA_CTL_PropertyKey_t, ct.POINTER(ct.c_int64), (size_t)]
        self.lib.SA_CTL_SetProperty_i64.argtypes = [SA_CTL_DeviceHandle_t, idx, SA_CTL_PropertyKey_t, ct.c_int64]

        self.lib.SA_CTL_GetProperty_i32.argtypes = [SA_CTL_DeviceHandle_t, idx, SA_CTL_PropertyKey_t, ct.POINTER(ct.c_int32), (size_t)]
        self.lib.SA_CTL_SetProperty_i32.argtypes = [SA_CTL_DeviceHandle_t, idx, SA_CTL_PropertyKey_t, ct.c_int32]

        self.lib.SA_CTL_GetProperty_s.argtypes = [SA_CTL_DeviceHandle_t, idx, SA_CTL_PropertyKey_t,
                                                    ct.c_char_p, ct.POINTER(size_t)]

    def _return_handler(self, func_name, ret_value):
        if self.lib.__getattribute__(func_name).restype != ct.c_void_p and (func_name not in _IGNORE_ERR):
            if ret_value > 0:
                try:
                    message = _ERRORS[ret_value]
                except KeyError:
                    message = 'Errorcode {}. Please lookup in manual page 266'.format(ret_value)
                raise InstrumentError(message)

    @Action()
    def find_devices(self):
        deviceList = bytes("".join(1024 * [" "]), encoding='utf8')
        ioDeviceListLen = ct.c_size_t(len(deviceList))
        self.lib.SA_CTL_FindDevices(bytes("", encoding='utf8'), deviceList, byref(ioDeviceListLen))
        return str(deviceList)[:ioDeviceListLen.value]

class MCS2_Bare(MCS2_Find_devices):
    """Only consists direct wrappers around library"""
    def __init__(self, device_locator=None, *args, **kwargs):
        """ Set default settings for device

        :param device_locator: string, eg:
                'usb:sn:<serial>'
                'usb:ix:<n>'
                'network:sn:<serial>'
                'network:<ip>'
        """
        super().__init__(*args, **kwargs)
        self.device_locator = device_locator
        self.dHandle = ct.c_uint32()
        self.dll = self.lib
        self.num_of_chan = None

    def initialize(self):
        """
        Initialize the piezo stage
        context will be passed to self.dHandle
        """
        self.lib.SA_CTL_Open(byref(self.dHandle), self.device_locator, "")

    def finalize(self):
        self.lib.SA_CTL_Close(self.dHandle)

    @Action()
    def move_channel(self, channel, value, tHandle=0):
        self.lib.SA_CTL_Move(self.dHandle, channel, int(value), tHandle)

    def getproperty_i64(self, channel, key):
        val = ct.c_int64()
        self.lib.SA_CTL_GetProperty_i64(self.dHandle, channel, key, byref(val), 0)
        return val.value

    def setproperty_i64(self, channel, key, val):
        self.lib.SA_CTL_SetProperty_i64(self.dHandle, channel, key, val)

    def getproperty_i32(self, channel, key):
        val = ct.c_int32()
        self.lib.SA_CTL_GetProperty_i32(self.dHandle, channel, key, byref(val), 0)
        return val.value

    def setproperty_i32(self, channel, key, val):
        self.lib.SA_CTL_SetProperty_i32(self.dHandle, channel, key, val)

    def getproperty_s(self, channel, key):
        val = bytes("".join(128 * [" "]), encoding='utf8')
        valLen = ct.c_size_t(len(val))
        self.lib.SA_CTL_GetProperty_s(self.dHandle, channel, key, val, byref(valLen))
        return str(val)[:valLen.value]

class MCS2_Minimum(MCS2_Bare):
    '''Contains some minimum functionallity in order to use with MCS2 and motion classes'''
    @Action()
    def read_position(self, channel):
        return self.getproperty_i64(channel, SmarActControlConstants.SA_CTL_PKEY_POSITION)

    def read_move_mode(self, channel):
        return self.getproperty_i32(channel, SmarActControlConstants.SA_CTL_PKEY_MOVE_MODE)

    def write_move_mode(self, channel, moveMode):
        self.setproperty_i32(channel, SmarActControlConstants.SA_CTL_PKEY_MOVE_MODE, moveMode)

    def channel_states(self, channel):
        state = self.getproperty_i32(channel, SmarActControlConstants.SA_CTL_PKEY_CHANNEL_STATE)
        states = [val for key, val in _STATES.items() if (key & state)]
        return states

    @Feat()
    def idn(self):
        return self.getproperty_s(0, SmarActControlConstants.SA_CTL_PKEY_DEVICE_NAME)


class MCS2_Axis(MotionAxisMultiple):
    @Feat(values=invert_dict(_MOVE_MODES))
    def move_mode(self):
        return self.parent.read_move_mode(self.num)

    @move_mode.setter
    def move_mode(self, moveMode):
        self.parent.write_move_mode(self.num, moveMode)

    @Feat(units='pm')
    def position(self):
        return self.parent.read_position(self.num)

    @position.setter
    def position(self, pos):
        """
        Waits until movement is done if self._config['wait_until_done'] = True.

        :param pos: new position
        """
        wait = self.wait_time if self._config['wait_until_done'] else None
        self._set_position(pos, wait=wait)

    def _write_position(self, pos):
        """
        Move stage to a certain position
        :param pos: New position
        """
        self.parent.move_channel(self.num, pos)

    @Feat()
    def states(self):
        return self.parent.channel_states(self.num)

    @Feat()
    def motion_done(self):
        if 'ACTIVELY_MOVING' in self.states:
            return False
        return True

    @Feat()
    def present(self):
        return 'SENSOR_PRESENT' in self.states


class MCS2(MCS2_Minimum, MotionControllerMultiAxis):
    """ Driver for MCS controller with multiple axis

    """

    def __init__(self, device_locator=None, *args, **kwargs):
        """ Set default settings for device

        :param device_locator: string, eg:
                'usb:sn:<serial>'
                'usb:ix:<n>'
                'network:sn:<serial>'
                'network:<ip>'
        """
        super().__init__(device_locator, *args, **kwargs)

    def initialize(self):
        super().initialize()
        print(self.idn)
        self.detect_axis()

    @Action()
    def detect_axis(self):
        """ Find the number of axis available.

        The detection stops as soon as an empty controller is found.
        """
        num = 0
        while True:
            axis = MCS2_Axis(parent=self, num=num,
                          id='{}.axis[{}]'.format(self.idn, num))
            if not axis.present:
                return

            self.axes.append(axis)

            # update units of axis NOT WORKING on 20190109
            #axis.update({'units': {**_POSITIONERS_ROTATION, **_POSITIONERS_TRANSLATION}[axis.type]['units']},
            #            force=True)

            num += 1

    # COPY FROM MotionControllerMultiAxis beacuse inheretence does not work
    @Feat(read_once=False)
    def position(self):
        return [axis.position for axis in self.axes]

    @Feat(read_once=False)
    def _position_cached(self):
        return [axis.recall('position') for axis in self.axes]

    @position.setter
    def position(self, pos):
        """Move to position (x,y,...)"""
        return self._position(pos)