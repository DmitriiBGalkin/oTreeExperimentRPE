from otree.api import *
from . import *
import random

class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield IntroductionGeneral
            yield IntroductionMarket
            yield IntroductionCalculator, dict(q1 = 1350, q2 = 44, q3 = 1222)
            yield IntroductionGame
            yield FirstGame
        if self.player.subsession.period == 1:
            yield NewSupergame
        yield Play, dict(UNITS=round(random.gauss(30,5)))

