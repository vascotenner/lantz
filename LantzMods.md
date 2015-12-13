# Internal bug fixes to lantz code #
Here's some modifications I've made to the stock Lantz codes to eliminate some bugs.

## Missing colorama imports ##
lantz/log.py add the line:

``
from colorama import Fore, Back, Style
``

This issue was actually originally addressed here: https://github.com/LabPy/lantz/issues/51 but not fixed in the next release.

TODO: put in a formal push to fix this in the main distribution.


## Changes to NIDAQ driver ##

Still working on a bug fix for this, but can tell what's going wrong.

Basically the GetTaskHandle() call fails because it truncates the TaskHandle to be a 32-bit integer, when the true value is 64-bit.

If anyone has an idea of how to fix this, that would be great.
