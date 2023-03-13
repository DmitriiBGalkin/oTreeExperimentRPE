from otree.api import *


doc = """
Your app description
"""
participant.vars

class C(BaseConstants):
    NAME_IN_URL = 'CournotSimple'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3
    INSTRUCTIONS_TEMPLATE = 'cournot/instructions.html'
    TOTAL_CAPACITY = 100
    GAMMA = 1
    COST = 0
    MAX_UNITS_PER_PLAYER = int(TOTAL_CAPACITY / PLAYERS_PER_GROUP)
    

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    MARKET_QUANTITY=models.IntegerField(doc="""Total units produced by all players""")



class Player(BasePlayer):
    units = models.IntegerField(
        min=0,
        max=C.MAX_UNITS_PER_PLAYER,
        doc="""Quantity of units to produce""",
        label="How many units will you produce (from 0 to 30)?",
    )

def set_payoffs(group):
    players = group.get_players()
    group.total_units = sum([p.units for p in players])
    group.unit_price = C.TOTAL_CAPACITY - group.total_units
    for p in players:
        p.payoff = group.unit_price * p.units



# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
