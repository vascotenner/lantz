# A Quick Primer on Setting Up Lantz #
Version: 1.0

Author: Peter Mintun (pmintun@uchicago.edu)

Date: 11/17/2015

I wrote this as a test file for GitHub before writing any real drivers. This is essentially a more explicit version of the documentation in Section 1.6: http://lantz.readthedocs.org/en/latest/tutorial/installing.html, it should be helpful for any Python novices hoping to get involved with writing drivers for the Lantz system. At some point, this will be updated to include more details about what National Instruments drivers need to be installed at a bare minimum (pending setting up a data computer from scratch).

Prerequisites: Don't have Windows 10! (at least not yet...)

# 1. Install Python 3 using Miniconda #
Install Python 3 using Miniconda. This will create a secondary Python distribution that is separate from other versions of Python that you might already have.

Download Python 3.5 from this link: http://conda.pydata.org/miniconda.html

Install Miniconda3 by following the instructions in the wizard. Make sure to note the directory that you install Miniconda3 to, you will need it for the next step.

# 2. Install some lantz dependencies using conda #
Open the Windows command prompt.

From the command line, cd to the directory that you installed Miniconda3 to in the previous step. Then enter the Scripts folder. If you list the files, there should be a file conda.exe.

Now install the packages for lantz using the command:

    > conda install pip numpy sphinx pyqt


This command will install a series of packages: pip (used for installation), numpy (used for numerical analysis), sphinx (a documentation tool), and pyqt (Python bindings for the Qt application framework). In addition, conda figures out the missing dependencies for these packages and install/configure them automatically.

After this is installed, you should have all the pieces necessary to run the basic functionality of lantz.

# 3. Install other packages using pip #

From the command line, run the command:

    > pip install colorama pyserial pyusb lantz

This command installs the colorama (used for producing colorful terminal output), pyserial (interfacing with serial devices), pyusb(interfacing with usb devices), and lantz (what you're supposedly hoping to install) packages to your Miniconda3 installation.

# 4. Install National Instruments Drivers #
TODO: write this section!

# 5 . Test your installation #
From the command prompt, move up a directory into your main Miniconda3 installation folder, then run `python.exe`

This should give you a Python 3.x command prompt!

Now run the command:

    >>> import lantz

This should import the lantz module. If this runs successfully, then you probably have installed lantz correctly.
