# -*- coding: utf-8 -*-
"""
    lantz.drivers.attocubes.anc350
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation of the drivers for the ANC350 controller

    This uses the 'anc350v3.dll' (not the v4 to be compatible with both the 32-bit and 64-bit DLL)

    Author: Alexandre Bourassa
    Date: 9/12/2016
"""
import ctypes as ct
from enum import Enum

from lantz import Driver, Feat, Action
from lantz.errors import InstrumentError
from lantz.foreign import Library, LibraryDriver, RetStr, RetValue

lib_name = 'anc350_dll/win64/anc350v3.dll'


#Enum list
class ACTUATOR_TYPE(Enum):
    ActLinear=0;ActGonio=1;ActRot=2
class DEVICE_TYPE(Enum):
    Anc350Res=0;Anc350Num=1;Anc350Fps=2;Anc350None=3
class INTERFACE_TYPE(Enum):
    IfNone=0;IfUsb=1;IfTcp=2;IfAll=3
class MOVING_STATUS(Enum):
    MoveIdle=0;MoveMove=1;MovePending=2
class ERROR_TYPE(Enum):
    ANC_Ok=0;ANC_Error=-1;ANC_Timeout=1;ANC_NotConnected=2;ANC_DriverError =3
    ANC_DeviceLocked=7; ANC_Unknown=8; ANC_NoDevice=9; ANC_NoAxis=10; ANC_OutOfRange=11
    ANC_NotAvailable = 12

class _common_lib_inst(LibraryDriver):
    LIBRARY_NAME = lib_name
_lib_inst = _common_lib_inst()
LIB = _lib_inst.lib
DEV_COUNT = RetValue('u32')
LIB.ANC_discover(INTERFACE_TYPE.IfAll.value, DEV_COUNT)
DEV_COUNT = DEV_COUNT.value

def list_ANC350_devices():
    #Query the info of all the devices
    devices = dict()
    for devNo in range(DEV_COUNT):
        print(devNo, type(devNo))

        devType=RetValue('i32')
        id=RetValue('i32')
        serialNo=RetValue('b')
        address=RetValue('b')
        connected=RetValue('?')
        LIB.ANC_getDeviceInfo(devNo, devType, id, serialNo, address, connected)
        devices[devNo] = {'devType':DEVICE_TYPE(devType.value).name, 'id':id.value, 'serialNo':serialNo.value, 'address':address.value, 'connected':connected.value}
    return devices


class ANC350(LibraryDriver):
    LIBRARY_NAME = lib_name

    def __init__(self, devNo, *args, **kwargs):
        Driver.__init__(self, *args, **kwargs)
        self.devNo = devNo
        self.handle = None

        #Need to discover devices before doing anything else
        #devCount, = self._call(LIB.ANC_discover, [INTERFACE_TYPE.IfAll.value], ['u32'])

        if self.devNo >= DEV_COUNT:
            raise Exception("Invalid devNo.  Try listing devices to see what's available")

    def _call(self, f, args, ret_args_types):
        ret_args = list()
        for t in ret_args_types:
            ret_args.append(RetValue(t))
        error_code, *vals = f(*args, *ret_args)
        if error_code == 0:
            return vals
        else:
            raise InstrumentError(ERROR_TYPE(error_code).name)

    @Action()
    def getDeviceInfo(self):
        ret = self._call(LIB.ANC_getDeviceInfo, [self.devNo], ['i32','i32','b','b','?'])
        return {'devType':ret[0], 'id':ret[1], 'serialNo':ret[2], 'address':ret[3],'connected':ret[4]}

    def initialize(self):
        handle = RetValue('i32')
        LIB.ANC_connect(self.devNo, handle)
