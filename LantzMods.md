# Internal bug fixes to lantz code #
Here's some modifications I've made to the stock Lantz codes to eliminate some bugs.

## Missing colorama imports ##
lantz/log.py add the line:

``
from colorama import Fore, Back, Style
``

This issue was actually originally addressed here: https://github.com/LabPy/lantz/issues/51 but not fixed in the next release.

TODO: put in a formal push to fix this in the main distribution.
