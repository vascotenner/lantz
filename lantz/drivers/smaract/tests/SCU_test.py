from lantz.drivers.smaract.smaract_motion_SCU import SCU, MotionAxis
import lantz
import time
import numpy as np
import lantz
import visa
import lantz.drivers.pi.piezo as pi
from pyvisa import constants

rm = visa.ResourceManager('@py')
lantz.messagebased._resource_manager = rm

#print('\n'.join([': '.join([key, str(val)]) for key, val in rm.list_resources_info().items()]))


try:
    lantzlog
except NameError:
    lantzlog = lantz.log.log_to_screen(level=lantz.log.DEBUG)



with SCU.via_serial(port="/dev/serial/by-id/usb-SmarAct_SmarAct_SCU-3D_FT2YP402-if00-port0") as smaract:
    smaract.idn
    for axis in smaract.axes[:]:
        axis.position
        axis.motion_done
        axis.wait_time
        axis.position = 500
        axis.calibrate_sensor()
        axis._wait_until_done()
        #axis.units
        #axis.units = 'degree'
        #axis.units
        pass
