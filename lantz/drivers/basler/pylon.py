# -*- coding: utf-8 -*-
"""
    lantz.drivers.basler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation for a basler camera via pypylon and pylon

    Requires:
    - pylon https://www.baslerweb.com/en/support/downloads/software-downloads/

    Log:
    Tried to implement PyPylon, but did not compile with python 3.5
    - PyPylon https://github.com/dihm/PyPylon (tested with version:
                        f5b5f8dfb179af6c23340fe81a10bb75f2f467f7)


    Author: Vasco Tenner
    Date: 20171208

    TODO:
    - 12 bit packet readout
    - Bandwith control
    - Dynamically add available feats
    - Dynamically set available values for feats
"""

from lantz.driver import Driver
# from lantz.foreign import LibraryDriver
from lantz import Feat, DictFeat, Action
# import ctypes as ct
import pypylon
import numpy as np


def todict(listitems):
    'Helper function to create dicts usable in feats'
    d = {}
    for item in listitems:
        d.update({item:item})
    return d

class Cam(Driver):
    # LIBRARY_NAME = '/opt/pylon5/lib64/libpylonc.so'

    def __init__(self, camera=0,
                 *args, **kwargs):
        """
        @params
        :type camera_num: int, The camera device index: 0,1,..

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

    @Feat()
    def info(self):
        # We can still get information of the camera back
        return 'Camera info of camera object:', self.cam.device_info

    @Feat(units='us')
    def exposure_time(self):
        return self.cam.properties['ExposureTimeAbs']

    @exposure_time.setter
    def exposure_time(self, time):
        self.cam.properties['ExposureTimeAbs'] = time

    @Feat()
    def gain(self):
        return self.cam.properties['GainRaw']

    @gain.setter
    def gain(self, value):
        self.cam.properties['GainRaw'] = value

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
