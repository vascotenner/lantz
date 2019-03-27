from lantz.drivers.alliedvision import list_cameras, VimbaCam

import lantz
import time
try:
        lantzlog
except NameError:
        lantzlog = lantz.log.log_to_screen(level=lantz.log.INFO)

ms = lantz.Q_('ms')
us = lantz.Q_('us')

if __name__ == '__main__':
    print(list_cameras())

    # test both expert and beginner
    cam = VimbaCam(camera='DEV_000F310349F5', level='expert')
    cam.initialize()
    cam.exposure_time
    cam.finalize()

    cam = VimbaCam(camera='DEV_000F310349F5', level='beginner')
    cam.initialize()
    cam.exposure_time
    cam.exposure_time = 3000
    cam.exposure_time = 4001.
    cam.exposure_time = 5001. * us
    cam.exposure_time += 1 * ms
    cam.exposure_time
    cam.gain = 10

    # test roi
    cam.set_roi(height=100, width=200, yoffset=10, xoffset=20)
    frame = cam.grab_image()
    print(frame.shape)
    assert frame.shape == (100, 200)
    #cam.set_roi(height=1400, width=200, yoffset=0, xoffset=0)
    cam.reset_roi()

    #cam.list_properties()
    for p, feature in cam.properties.items():
        if feature.info.unit is not None:
            print(p)
    frame = cam.grab_image()
    print(frame.shape)
    print(cam.feats['PixelFormat'].values)
    cam.PixelFormat = 'Mono8'
    print('PixelFormat: ', cam.PixelFormat)
    print('Reduce log level')
    lantzlog.level = lantz.log.WARNING
    print('Speedtest:')
    nr = 10000
    start = time.time()
    for n in range(nr):
        frame = cam.grab_image()
        mean = frame.mean()
        duration = (time.time() - start) * 1000 * lantz.Q_('ms')
        print('Read {} images in {}. Reading alone took {}. Framerate {}. Mean of last frame {}'.format(n,
                                                                                 duration,
                                                                                 duration - n * cam.exposure_time,
                                                                                 n / duration.to('s'),
                                                                                 mean,),)

    cam.finalize()
