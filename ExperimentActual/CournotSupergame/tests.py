from otree.api import *

class PlayerBot(Bot):
    def play_round(self):
        yield NewSupergame

        yield Play, dict(UNITS=20)

        yield ResultsWaitPage

        yield FinalResultsPage
