# -*- coding: utf-8 -*-
"""
    lantz.drivers.alliedvision
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implementation for a alliedvision camera via pymba and pylon

    Requires:
    - pymba: https://github.com/morefigs/pymba
    - vimba: https://www.alliedvision.com/en/products/software.html

    Log:
    - create same API as lantz.drivers.basler


    Author: Vasco Tenner
    Date: 20181204

    TODO:
    - Test
    - 12 bit packet readout
    - Bandwith control
    - Dynamically set available values for feats
"""

from lantz.driver import Driver
from lantz import Feat, DictFeat, Action
from pymba import Vimba
import pymba
import numpy as np
import threading
import time


beginner_controls = ['ExposureTimeAbs', 'GainRaw', 'Width', 'Height',
                     'OffsetX', 'OffsetY']
aliases = {
            'pixel_format': 'PixelFormat',
            'gain': 'Gain',
          }

# add all aliases to beginner_controls
for val in aliases.values():
    if val not in beginner_controls:
        beginner_controls += [val]

ignore_limits = ['OffsetX', 'OffsetY', 'Width', 'Height']

def todict(listitems):
    'Helper function to create dicts usable in feats'
    d = {}
    for item in listitems:
        d.update({item: item})
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
        return self.cam.feature(p).value
    return tmpfunc


def create_setter(p):
    def tmpfunc(self, val):
        self.cam.feature(p).value = val
    return tmpfunc


def list_cameras():
    with Vimba() as vimba:
        return vimba.camera_ids()

class VimbaCam(Driver):

    def __init__(self, camera=0, level='beginner',
                 *args, **kwargs):
        """
        @params
        :type camera_num: int, The camera device index: 0,1,..
        :type level: str, Level of controls to show ['beginner', 'expert']

        Example is found in
        lantz/drivers/alliedvision/tests/vimbatest.py
        """
        super().__init__(*args, **kwargs)
        self.camera = camera
        self.level = level
        # Some actions cannot be performed while reading
        self._grabbing_lock = threading.RLock()
        self.frame = None
        self.cam = None

    def initialize(self):
        """
        Params:
        camera -- number in list of show_cameras or friendly_name
        """

        self.vimba = Vimba()
        self.vimba.startup()

        self.cam = self.vimba.camera(self.camera)
        self.cam.open()

        self._dynamically_add_properties()
        self._aliases()

        # Go to full available speed
        # cam.properties['DeviceLinkThroughputLimitMode'] = 'Off'

    def finalize(self):
        #self.cam.revoke_all_frames()
        self.cam.close()
        self.vimba.shutdown()
        return

    def _dynamically_add_properties(self):
        """Add all properties available on driver as Feats"""
        props = self.cam.feature_names() if self.level == 'expert' else beginner_controls
        for p in props:
            feature = self.cam.feature(p)
            info = feature.info
            try:
                value = feature.value
                range_ = feature.range

                # alternatively the feature value can be read as an object attribute
                # value = getattr(camera, feature_name)
                # or
                # value = camera.someFeatureName

            except pymba.VimbaException as e:
                value = e
                range_ = None

            # Some limits are set dynamically. The current Feat cannot support this. Lets ignore the limits for those features
            limits = range_ if isinstance(range_, tuple) and p not in ignore_limits else None
            values = todict(range_) if isinstance(range_, list) else None

            feat = Feat(fget=create_getter(p),
                        fset=create_setter(p),
                        doc=info.description,
                        units=info.unit,
                        limits=limits,
                        values=values,
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
        return 'Camera info of camera object:', self.cam.getInfo()  # TODO TEST

    # Most properties are added automatically by _dynamically_add_properties

    # VimbaC does not report units for the exposure time, only mention us in description
    @Feat(units='us')
    def exposure_time(self):
        return self.ExposureTimeAbs

    @exposure_time.setter
    def exposure_time(self, val):
        print('Set expopsuretime to ', val)
        self.ExposureTimeAbs = val

    @Feat()
    def properties(self):
        """Dict with all properties supported by pylon dll driver"""
        props = self.cam.feature_names()
        return {p: self.cam.feature(p) for p in props}

    @Action()
    def list_properties(self):
        """List all properties and their values"""
        for key, feature in self.properties.items():
            try:

                range_ = feature.range
                value = feature.value
            except pymba.VimbaException as e:
                value = e
                range_ = None
                #value = '<NOT READABLE>'
            description = feature.info.description

            print('{0} ({1}):\t{2}\t{3}'.format(key, description, value, range_))

    #@Action()
    #def renew_frame(self):
    #    '''Create a new frame buffer when the pxformat changes'''
    #    pass
        #self.cam.revoke_all_frames()
        #self.frame = self.cam.create_frame()
        #self.frame.announce()

    @Action()
    def arm(self, mode='SingleFrame'):
        """Prepare the camera to capture frames"""
        self.cam.arm(mode)

    @Action()
    def disarm(self):
        self.cam.disarm()

    @Action(log_output=False)
    def grab_image(self):
        """Record a single image from the camera"""
        with self._grabbing_lock:
            self.arm(mode='SingleFrame')
            image = self.grab_frame()
            self.disarm()
        return image

    @Action(log_output=False)
    def grab_frame(self):
        """Grab a single frame and convert it to numpy array. Camera should be armed"""
        frame = self.cam.acquire_frame()
        image = frame.buffer_data_numpy()
        return image

    @Action(log_output=False)
    def grab_images(self, num=1):
        with self._grabbing_lock:
            self.arm(mode='SingleFrame')
            images = [self.grab_frame() for i in range(num)]
            self.disarm()
        return images

    @Action(log_output=False)
    def getFrame(self):
        """Backward compatibility"""
        return self.grab_image()

    @Action()
    def set_roi(self, height, width, yoffset, xoffset):
        # Validation:
        if width + xoffset > self.properties['WidthMax'].value:
            self.log_error('Not setting ROI:  Width + xoffset = {} exceeding '
                           'max width of camera {}.'.format(width + xoffset,
                                                            self.properties['WidthMax'].value))
            return
        if height + yoffset > self.properties['HeightMax'].value:
            self.log_error('Not setting ROI: Height + yoffset = {} exceeding '
                           'max height of camera {}.'.format(height + yoffset,
                                                             self.properties['HeightMax'].value))
            return

        # Offset should be multiple of 2:
        xoffset -= xoffset % 2
        yoffset -= yoffset % 2

        if height < 16:
            self.log_error('Height {} too small, smaller than 16. Adjusting '
                           'to 16'.format(height))
            height = 16
        if width < 16:
            self.log_error('Width {} too small, smaller than 16. Adjusting '
                           'to 16'.format(width))
            width = 16

        with self._grabbing_lock:
            # Order matters!
            if self.OffsetY > yoffset:
                self.OffsetY = yoffset
                self.Height = height
            else:
                self.Height = height
                self.OffsetY = yoffset
            if self.OffsetX > xoffset:
                self.OffsetX = xoffset
                self.Width = width
            else:
                self.Width = width
                self.OffsetX = xoffset

    @Action()
    def reset_roi(self):
        """Sets ROI to maximum camera size"""
        self.set_roi(self.properties['HeightMax'].value,
                     self.properties['WidthMax'].value,
                     0,
                     0)

    # Helperfunctions for ROI settings
    def limit_width(self, dx):
        if dx > self.properties['WidthMax'].value:
            dx = self.properties['WidthMax'].value
        elif dx < 16:
            dx = 16
        return dx

    def limit_height(self, dy):
        if dy > self.properties['HeightMax'].value:
            dy = self.properties['HeightMax'].value
        elif dy < 16:
            dy = 16
        return dy

    def limit_xoffset(self, xoffset, dx):
        if xoffset < 0:
            xoffset = 0
        if xoffset + dx > self.properties['WidthMax'].value:
            xoffset = self.properties['WidthMax'].value - dx
        return xoffset

    def limit_yoffset(self, yoffset, dy):
        if yoffset < 0:
            yoffset = 0
        if yoffset + dy > self.properties['HeightMax'].value:
            yoffset = self.properties['HeightMax'].value - dy
        return yoffset

    @Action()
    def calc_roi(self, center=None, size=None, coords=None):
        """Calculate the left bottom corner and the width and height
        of a box with center (x,y) and size x [(x,y)]. Respects device
        size"""
        if center and size:
            y, x = center
            try:
                dy, dx = size
            except TypeError:
                dx = dy = size

            # Make sizes never exceed camera sizes
            dx = self.limit_width(dx)
            dy = self.limit_width(dy)

            xoffset = x - dx // 2
            yoffset = y - dy // 2

            xoffset = self.limit_xoffset(xoffset, dx)
            yoffset = self.limit_yoffset(yoffset, dy)

            return dy, dx, yoffset, xoffset

        elif coords:
            xoffset = int(coords[1][0])
            dx = int(coords[1][1] - xoffset)

            yoffset = int(coords[0][0])
            dy = int(coords[0][1] - yoffset)

            # print(dy,dx)
            dx = self.limit_width(dx)
            dy = self.limit_height(dy)

            # print(yoffset, xoffset)
            xoffset = self.limit_xoffset(xoffset, dx)
            yoffset = self.limit_yoffset(yoffset, dy)

            return dy, dx, yoffset, xoffset

        else:
            raise ValueError('center&size or coords should be supplied')

    def calc_roi_from_rel_coords(self, relcoords):
        """Calculate the new ROI from coordinates relative to the current
        viewport"""

        coords = ((self.OffsetY + relcoords[0][0],
                   self.OffsetY + relcoords[0][1]),
                  (self.OffsetX + relcoords[1][0],
                   self.OffsetX + relcoords[1][1]))
        # print('Rel_coords says new coords are', coords)
        return self.calc_roi(coords=coords)
