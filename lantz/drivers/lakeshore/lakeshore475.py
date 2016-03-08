from lantz import Feat
from lantz.messagebased import MessageBasedDriver

class Lakeshore475(MessageBasedDriver):

    @Feat(units='gauss')
    def field(self):
        return self.query('RDGFIELD?')
