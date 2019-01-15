from lantz.drivers.smaract.MCS2 import MCS2_Minimum, MCS2_Axis, MCS2_Find_devices, MCS2
import lantz
import time
import pint

nm = lantz.Q_('nm')

try:
    lantzlog
except NameError:
    lantzlog = lantz.log.log_to_screen(level=lantz.log.DEBUG)


#"usb:sn:MCS2-00000819"

fd = MCS2_Find_devices()
fd.initialize()
devices = fd.find_devices()
fd.finalize()

#with MCS2_Bare('usb:ix:1') as smaract:
with MCS2_Minimum("usb:sn:MCS2-00000819") as smaract:
    print(smaract.find_devices())
    print(smaract.idn)
    # Output is provided by log
    smaract.read_position(1)
    #smaract.move_channel(1, 10000, 0)
    smaract.read_position(1)
    axis = MCS2_Axis(parent=smaract, num=1, id='a', config={'accuracy': 10000  # pm
                                                            })
    #axis.units = 'pm'
    axis.position
    axis.move_mode
    axis.states
    #smaract.move_channel(1, 100000, 0)
    #for i in range(10):
    #    axis.states
    #    time.sleep(0.01)
    axis.position += 10*nm
    #print(smaract.find_devices())

    axis2 = MCS2_Axis(parent=smaract, num=3, id='rotation', config={'accuracy': 10000  # pm
                                                           })
    axis2.position
    axis2.move_mode
    axis2.states

with MCS2("usb:sn:MCS2-00000819") as smaract:
    smaract.position