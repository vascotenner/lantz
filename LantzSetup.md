# A Quick Primer on Setting Up Lantz #
Version: 1.0

Author: Peter Mintun (pmintun@uchicago.edu)

Date: 11/17/2015

I wrote this as a test file for GitHub before writing any real drivers. This is essentially a more explicit version of the documentation in Section 1.6: http://lantz.readthedocs.org/en/latest/tutorial/installing.html, it should be helpful for any Python novices hoping to get involved with writing drivers for the Lantz system. At some point, this will be updated to include more details about what National Instruments drivers need to be installed at a bare minimum (pending setting up a data computer from scratch).

Prerequisites: Don't have Windows 10! (at least not yet...)

## 1. Install Python 3 using Miniconda ##
Install Python 3 using Miniconda. This will create a secondary Python distribution that is separate from other versions of Python that you might already have.

Download Python 3.5 from this link: http://conda.pydata.org/miniconda.html

Install Miniconda3 by following the instructions in the wizard. Make sure to note the directory that you install Miniconda3 to, you will need it for the next step.

## 2. Install some lantz dependencies using conda ##
Open the Windows command prompt.

From the command line, cd to the directory that you installed Miniconda3 to in the previous step. Then enter the Scripts folder. If you list the files, there should be a file conda.exe.

Now install the packages for lantz using the command:

    > conda install pip numpy sphinx pyqt


This command will install a series of packages: pip (used for installation), numpy (used for numerical analysis), sphinx (a documentation tool), and pyqt (Python bindings for the Qt application framework). In addition, conda figures out the missing dependencies for these packages and install/configure them automatically.

After this is installed, you should have all the pieces necessary to run the basic functionality of lantz.

### Possible Issues and Solutions ###

If `pyqt` fails to install, put a copy of `qt.conf` in `Library\Bin`. Thanks to @varses for this tip!

## 3. Install other packages using pip ##

From the command line, run the command:

    > pip install colorama pyserial pyusb lantz

This command installs the colorama (used for producing colorful terminal output), pyserial (interfacing with serial devices), pyusb(interfacing with usb devices), and lantz (what you're supposedly hoping to install) packages to your Miniconda3 installation.

## 4 . Test your installation ##
From the command prompt, move up a directory into your main Miniconda3 installation folder, then run `python.exe`

This should give you a Python 3.x command prompt!

Now run the command:

    >>> import lantz

This should import the lantz module. If this runs successfully, then you probably have installed lantz correctly.

## 5. Install National Instruments Drivers ##
This seciton will might vary, depending on what NI device(s) you're trying to install, but I've included my setup information here for help.

### 5.1 Installing GPIB Devices ###
I needed to install NI-488.2 version 15.0.0 for my National Instruments GPIB-USB-HS device (USB to GPIB interface). This package includes the drivers needed to interface with GPIB hardware, including the very useful NIMAX utility.

First, download it from: http://www.ni.com/download/ni-488.2-15.0/5427/en.

Next, right click on the file you downloaded and select "Run as Administrator". Select a destination folder (change it from the default if you want) to unzip the download files into. This will then start the installation wizard. This will install a bunch of stuff by default, so configure the installation to not install stuff you won't be needing (anything to interface with LabVIEW, for starters =P ).

Once the wizard completes, you'll need to restart. I would also recommend installing an NI-488.2 patches that come up from the National Instruments software update.

After doing this, you should be able run NI MAX and see a GPIB device that's connected by clicking on the Scan for Instruments button after selecting your GPIB device.

### 5.2 Installing DAQ Devices ###
The DAQ I set up was a NI USB-6343.

First, install the NIDAQmx 15.0.1 software, downloaded from: http://www.ni.com/download/ni-daqmx-15.0.1/5353/en.

Next, right click on the file you downloaded and select "Run as Administrator". Select a destination folder (change it from the default if you want) to unzip the download files into. This will then start the installation wizard. This might install a bunch of stuff by default, so configure the installation to not install stuff you won't be needing (anything to interface with LabVIEW, for starters =P ).

After the installation wizard completes, you'll need to restart. Windows should recognize your DAQ device after rebooting. From there, you should be able to use the NI Device Manager/Test Panel applications to query the ports on your device.

# 6. Start running Lantz! #
Stay safe and happy data acquisition!
