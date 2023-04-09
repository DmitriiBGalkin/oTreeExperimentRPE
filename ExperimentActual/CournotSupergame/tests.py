from otree.api import *
from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        if self.player.subsession.period == 1:
            yield NewSupergame
        yield Play, dict(UNITS=random.gauss(30,5))

