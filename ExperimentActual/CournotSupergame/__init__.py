from otree.api import *
import random
import itertools

doc = """
Cournot Supergames 
"""
def cumsum(lst):
    total = 0
    new = []
    for ele in lst:
        total += ele
        new.append(total)
    return new

def random_numbers_until():
    numbers = []
    while True:
        number = random.randint(1, 9)
        numbers.append(number)
        if number == 9:
            break
    return numbers
def repeat_elements_in_sublists(lst, reps):
    new_lst = []
    for sub_lst in lst:
        new_sub_lst = []
        for i, element in enumerate(sub_lst):
            new_sub_lst.extend([element]*reps[i])
        new_lst.append(new_sub_lst)
    return new_lst

#The above function draws random numbers from 1-10 and stops when it hits 10.

SUPERGAME_1 = random_numbers_until()
SUPERGAME_2 = random_numbers_until()
SUPERGAME_3 = random_numbers_until()
SUPERGAME_4 = random_numbers_until()
#Creating 4 sequences for block randomisation

print(SUPERGAME_1,SUPERGAME_2,SUPERGAME_3,SUPERGAME_4)

class C(BaseConstants):
    NAME_IN_URL = 'supergames'
    PLAYERS_PER_GROUP = 2
    MIN_ROUNDS=10
    ROUNDS_PER_SG = [max(MIN_ROUNDS, len(SUPERGAME_1)), max(MIN_ROUNDS, len(SUPERGAME_2)), max(MIN_ROUNDS, len(SUPERGAME_3)), max(MIN_ROUNDS, len(SUPERGAME_4))]
    #In the ROUNDS_PER_SG each supergame consist of at least 10 rounds. If there are less rounds in the supergame, then only those up to the len(supergame) would be payoff-relevant
    SG_ENDS = cumsum(ROUNDS_PER_SG)
    print('SG_ENDS is', SG_ENDS)
    NUM_ROUNDS = sum(ROUNDS_PER_SG)
    POSSIBLE_CONTRACT_ALLOCATIONS = [["AA", "AR", "RA", "RR"],
                                     ["AR", "AA", "RA", "RR"],
                                     ["AA", "AR", "RR", "RA"],
                                     ["AR", "AA", "RR", "RA"],
                                     ["RA", "RR", "AA", "AR"],
                                     ["RA", "RR", "AR", "AA"],
                                     ["RR", "RA", "AA", "AR"],
                                     ["RR", "RA", "AR", "AA"]]
    POSSIBLE_CONTRACT_ORDERS_THROUGH_ALL_SUPERGAMES = repeat_elements_in_sublists(POSSIBLE_CONTRACT_ALLOCATIONS, ROUNDS_PER_SG)
    ITERATED_POSSIBLE_CONTRACT_ORDERS_THROUGH_ALL_SUPERGAMES = itertools.cycle(POSSIBLE_CONTRACT_ORDERS_THROUGH_ALL_SUPERGAMES)
    ITERARED_CONTRACT_ORDERS = itertools.cycle(POSSIBLE_CONTRACT_ALLOCATIONS)
    #Logic: There are 8 possible orders of how the contracts can be allocated for each supergame. "Repeat elements in the sublist" function then duplicates each contract according to how many rounds are played in a particular supergame.
    #We then assign this list to a participant. When we need to know which contract he is playing in round i, we just call this list[i].
    #The next step is to organise the groups and then reshuffle them for each supergame
class Subsession(BaseSubsession):
    sg = models.IntegerField()
    period = models.IntegerField()
    is_last_period = models.BooleanField()



def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        player.participant.CONTRACT_ORDER = ", ".join(next(C.ITERARED_CONTRACT_ORDERS))
        player.CONTRACTUAL_ORDER_FOR_THIS_PLAYER = next(C.ITERATED_POSSIBLE_CONTRACT_ORDERS_THROUGH_ALL_SUPERGAMES)
        #Assigning each player
        player.type = player.participant.CONTRACT_ORDER
    if subsession.round_number == 1:
        sg = 1
        period = 1
        # loop over all subsessions
        for ss in subsession.in_rounds(1, C.NUM_ROUNDS):
            ss.sg = sg
            ss.period = period
            # 'in' gives you a bool. for example: 5 in [1, 5, 6] # => True
            is_last_period = ss.round_number in C.SG_ENDS
            ss.is_last_period = is_last_period
            if is_last_period:
                sg += 1
                period = 1
            else:
                period += 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    type = models.StringField()

class NewSupergame(Page):
    wait_for_all_groups = True
    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.period == 1


class Play(Page):
    pass


page_sequence = [NewSupergame, Play]
