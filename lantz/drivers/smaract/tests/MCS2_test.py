from lantz.drivers.smaract.MCS2 import MCS2_Bare
import lantz
import time

try:
    lantzlog
except NameError:
    lantzlog = lantz.log.log_to_screen(level=lantz.log.DEBUG)


#"usb:sn:MCS2-00000819"


#with MCS2_Bare('usb:ix:1') as smaract:
with MCS2_Bare("usb:sn:MCS2-00000819") as smaract:
    print(smaract.find_devices())