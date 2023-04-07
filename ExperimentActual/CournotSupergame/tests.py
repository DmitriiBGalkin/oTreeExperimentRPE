from otree.api import *
from . import *

class PlayerBot(Bot):
    def play_round(self):
        yield NewSupergame

        yield Play, dict(UNITS=20)

