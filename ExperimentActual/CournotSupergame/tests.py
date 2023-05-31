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
            yield NewSupergame, dict()
        yield Play, dict(UNITS=round(random.gauss(30,5)))
        if self.round_number == C.NUM_ROUNDS:
            yield Questionnaire, dict(codeU1_firstletter='a', codeU1_secondletter='a', codeU1_penletter='a', codeU1_lastletter='a', codeU2_birthday=1, codeU3_firstletter='a', codeU3_secondletter='a', codeU4_firstletter='a', codeU4_secondletter='a', codeU4_penletter='a', codeU4_lastletter='a', codeU5_birthday=1, codeU6_birthday=1, codeU7_firstletter='a', codeU7_secondletter='a', codeU8_siblings='Ja', codeU9_order='First')
        if self.round_number == C.NUM_ROUNDS:
            yield FinalResultsPage

