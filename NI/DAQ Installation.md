# DAQ Installation Guide #
Author: Peter Mintun (pmintun@uchicago.edu)

Date: 12/14/2015

This guide details the steps needed to hack the existing Lantz driver to work on a 64-bit system.

## Installing Modified Lantz NI driver ##
If you are using Miniconda, the Lantz NI drivers will be installed at: `<Your Miniconda Directory>\Lib\site-packages\lantz\drivers\ni`

You will need to download the files in the NI64 folder from this repository and copy them to this location.

Basically, there's only one change to the existing driver on GitHub:
base.py - changed return value to uInt64 to accommodate 64-bit pointer type.
constants.py - no changes
channels.py - no changes
tasks.py - no changes

Also take the `foreign.py` file and replace the base lantz `foreign.py` file, this is located in
 `<Your Miniconda Directory>\Lib\site-packages\lantz\`


## Copy over 64-bit Libraries ##
*I'm not sure if this step is necessary, but this will ensure that your code actually links to the 64-bit versions of the DAQ libraries. Someone should actually try this guide without doing this step just to see.*

Search for the 64-bit version of nicaiu.dll and NIDAQmx.lib and add them to the Lantz `daqmx` folder: `<Your Miniconda Directory>\Lib\site-packages\lantz\drivers\ni\daqmx`


## Run Test Codes ##
There are two test scripts I've adapted from the Lantz library for testing out the DAQ.

`DAQ_info.py` will output a list of attributes for the DAQ, you can run it using the command:
```
python DAQ_info.py
```

`DAQ_demo.py` will read a single analog input data point from one of the analog in system channels, you can run it with:
```
python DAQ_demo.py 'dev1/ai0'
```
where 'dev1' is your DAQ device name and 'ai0' is the analog input channel you want to read.

`DAQ_blit.py` is a demo of sampling from the DAQ and live plotting the data w/ matplotlib.

## More Advanced Testing ##
Currently working on a more advanced test script to demonstrate some more advanced features of the DAQ.
