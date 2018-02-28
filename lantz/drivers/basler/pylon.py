# -*- coding: utf-8 -*-
"""
    lantz.drivers.basler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation for a basler camera via pypylon and pylon

    Requires:
    - pylon https://www.baslerweb.com/en/support/downloads/software-downloads/

    Log:
    - Dynamically add available feats
    - Collect single and multiple images
    - Set Gain and exposure time
    - PyPylon https://github.com/dihm/PyPylon (tested with version:
                        f5b5f8dfb179af6c23340fe81a10bb75f2f467f7)


    Author: Vasco Tenner
    Date: 20171208

    TODO:
    - 12 bit packet readout
    - Bandwith control
    - Dynamically set available values for feats
    - Set ROI
"""

from lantz.driver import Driver
# from lantz.foreign import LibraryDriver
from lantz import Feat, DictFeat, Action
# import ctypes as ct
import pypylon
import numpy as np


beginner_controls = ['ExposureTimeAbs', 'GainRaw', 'Width', 'Height',
                     'OffsetX', 'OffsetY']
property_units = {'ExposureTimeAbs': 'us', }
aliases = {'exposure_time': 'ExposureTimeAbs',
           'gain': 'GainRaw',
          }

def todict(listitems):
    'Helper function to create dicts usable in feats'
    d = {}
    for item in listitems:
        d.update({item:item})
    return d

def attach_dyn_propr(instance, prop_name, propr):
    """Attach property proper to instance with name prop_name.

    Reference: 
    * https://stackoverflow.com/a/1355444/509706
    * https://stackoverflow.com/questions/48448074
    """
    class_name = instance.__class__.__name__ + 'C'
    child_class = type(class_name, (instance.__class__,), {prop_name: propr})

    instance.__class__ = child_class

def create_getter(p):
    def tmpfunc(self):
        return self.cam.properties[p]
    return tmpfunc

def create_setter(p):
    def tmpfunc(self, val):
        self.cam.properties[p] = val
    return tmpfunc


class Cam(Driver):
    # LIBRARY_NAME = '/opt/pylon5/lib64/libpylonc.so'

    def __init__(self, camera=0, level='beginner',
                 *args, **kwargs):
        """
        @params
        :type camera_num: int, The camera device index: 0,1,..
        :type level: str, Level of controls to show ['beginner', 'expert']

        Example:
        import lantz
        from lantz.drivers.basler import Cam
        import time
        try:
                lantzlog
        except NameError:
                lantzlog = lantz.log.log_to_screen(level=lantz.log.DEBUG)

        cam = Cam(camera='Basler acA4112-8gm (40006341)')
        cam.initialize()
        cam.exposure_time
        cam.exposure_time = 3010
        cam.exposure_time
        next(cam.grab_images())
        cam.grab_image()
        print('Speedtest:')
        nr = 10
        start = time.time()
        for n in cam.grab_images(nr):
            n
            duration = (time.time()-start)*1000*lantz.Q_('ms')
            print('Read {} images in {}. Reading alone took {}. Framerate {}'.format(nr,
                duration, duration - nr* cam.exposure_time, nr / duration.to('s')))
                cam.finalize()
        """
        super().__init__(*args, **kwargs)
        self.camera = camera
        self.level = level

    def initialize(self):
        '''
        Params:
        camera -- number in list of show_cameras or friendly_name
        '''

        cameras = pypylon.factory.find_devices()
        self.log_debug('Available cameras are:' + str(cameras))

        try:
            if isinstance(self.camera, int):
                cam = cameras[self.camera]
                self.cam = pypylon.factory.create_device(cam)
            else:
                try:
                    cam = [c for c in cameras if c.friendly_name == self.camera][0]
                    self.cam = pypylon.factory.create_device(cam)
                except IndexError:
                    self.log_error('Camera {} not found in cameras: {}'.format(self.camera, cameras))
                    return
        except RuntimeError as err:
            self.log_error(err)
            raise RuntimeError(err)

        self.camera = cam.friendly_name

        # First Open camera before anything is accessable
        self.cam.open()

        self._dynamically_add_properties()
        self._aliases()

        # get rid of Mono12Packed and give a log error:
        fmt = self.pixel_format
        if fmt == str('Mono12Packed'):
            self.log_error('PixelFormat {} not supported. Using Mono12 instead'.format(fmt))
            self.pixel_format = 'Mono12'

        # Go to full available speed
        # cam.properties['DeviceLinkThroughputLimitMode'] = 'Off'

    def finalize(self):
        self.cam.close()
        return

    def _dynamically_add_properties(self):
        '''Add all properties available on driver as Feats'''
        # What about units?
        props = self.properties.keys() if self.level == 'expert' else beginner_controls
        for p in props:
            feat = Feat(fget=create_getter(p),
                        fset=create_setter(p),
                        doc=self.cam.properties.get_description(p),
                        units=property_units.get(p, None),
                        )
            feat.name = p
            attach_dyn_propr(self, p, feat)

    def _aliases(self):
        """Add easy to use aliases to strange internal pylon names

        Note that in the Logs, the original is renamed to the alias"""
        for alias, orig in aliases.items():
            attach_dyn_propr(self, alias, self.feats[orig].feat)


    @Feat()
    def info(self):
        # We can still get information of the camera back
        return 'Camera info of camera object:', self.cam.device_info

#    @Feat(units='us')
#    def exposure_time(self):
#        return self.cam.properties['ExposureTimeAbs']
#
#    @exposure_time.setter
#    def exposure_time(self, time):
#        self.cam.properties['ExposureTimeAbs'] = time
#
#    @Feat()
#    def gain(self):
#        return self.cam.properties['GainRaw']
#
#    @gain.setter
#    def gain(self, value):
#        self.cam.properties['GainRaw'] = value

    @Feat(values=todict(['Mono8','Mono12','Mono12Packed']))
    def pixel_format(self):
        fmt = self.cam.properties['PixelFormat']
        if fmt == 'Mono12Packed':
            self.log_error('PixelFormat {} not supported. Use Mono12 instead'.format(fmt))
        return fmt

    @pixel_format.setter
    def pixel_format(self, value):
        if value == 'Mono12Packed':
            self.log_error('PixelFormat {} not supported. Using Mono12 instead'.format(value))
            value = 'Mono12'
        self.cam.properties['PixelFormat'] = value

    @Feat()
    def properties(self):
        'Dict with all properties supported by pylon dll driver'
        return self.cam.properties
    
    @Action()
    def list_properties(self):
        'List all properties and their values'
        for key in self.cam.properties.keys():
            try:
                value = self.cam.properties[key]
            except IOError:
                value = '<NOT READABLE>'

            print('{0} ({1}):\t{2}'.format(key,
                            self.cam.properties.get_description(key), value))

    @Action(log_output=False)
    def grab_image(self):
        return next(self.cam.grab_images(1))

    @Action(log_output=False)
    def grab_images(self, num=1):
        return self.cam.grab_images(num)
