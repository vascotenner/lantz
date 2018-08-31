# -*- coding: utf-8 -*-
"""
    lantz.drivers.basler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Wraps Basler's pylon library using pypylon to provide lantz-style camera driver.

    Author: Peter Mintun
    Date: 9/21/2017
"""

from lantz.driver import Driver
from lantz import Feat, DictFeat, Action

import numpy as np

import pypylon

class BaslerCam(Driver):

    def initialize(self):
        #print('Build against pylon library version:', pypylon.pylon_version.version)

        available_cameras = pypylon.factory.find_devices()
        #print('Available cameras are', available_cameras)

        # Grep the first one and create a camera for it
        self.cam = pypylon.factory.create_device(available_cameras[-1])

        self.cam.open()
        self.cam.properties['PixelFormat'] = 'RGB8'
        self.cam.properties['DeviceLinkThroughputLimitMode'] = 'Off'

        return

    def list_properties(self):
        """
        Utility function to pull all available options from the camera and
        print them.
        """

        for key in self.cam.properties.keys():
            try:
                value = self.cam.properties[key]
            except IOError:
                value = '<NOT READABLE>'

            print('{0} ({1}):\t{2}'.format(key, self.cam.properties.get_description(key), value))

    def finalize(self):
        self.cam.close()
        return

    @Action()
    def getFrame(self):
        try:
            frame = self.cam.grab_images(1)
            #self.next_frame = frame.next()
            return frame
        except:
            return None

        return None



def test():

    cam = BaslerCam()
    cam.initialize()

    for image in cam.getFrame():

        print(image)

    cam.finalize()

if __name__ == '__main__':

    test()
