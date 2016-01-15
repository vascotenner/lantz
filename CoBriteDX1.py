from lantz import Feat, DictFeat, Action
from lantz.messagebased import MessageBasedDriver

from time import sleep


class CoBriteDX1(MessageBasedDriver):
    """

    """
    DEFAULTS = {'ASRL': {'write_termination': '\r',
                         'read_termination': '',
                        }}

    def initialize(self):
        """
        """
        super().initialize()

    




if __name__ == '__main__':
    with CoBriteDX1('USB:XXYYZZ') as inst:

            # inst.nm = 400.0
