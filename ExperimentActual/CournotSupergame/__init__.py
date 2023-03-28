from otree.api import *
import random
import itertools

doc = """   
Cournot Supergames asdasdasdads
"""
# setting the average number of rounds (i.e. through a max value on a die)
NUMBER_ROS = 10


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
        number = random.randint(1, NUMBER_ROS)
        numbers.append(number)
        if number == NUMBER_ROS:
            break
    return numbers


# The above function draws random numbers from 1-10 and stops when it hits 10.

def repeat_elements_in_sublists(lst, reps):
    new_lst = []
    for sub_lst in lst:
        new_sub_lst = []
        for i, element in enumerate(sub_lst):
            new_sub_lst.extend([element] * reps[i])
        new_lst.append(new_sub_lst)
    return new_lst


# The above function repeates the strings

def calculate_game_starts(rounds_per_game):
    game_starts = [1]
    for i in range(1, len(rounds_per_game)):
        game_starts.append(game_starts[-1] + rounds_per_game[i - 1])
    return game_starts


# Calculate supergames first rounds

def return_lists(my_list):
    result_list = []
    for i in range(len(my_list[0])):
        result_list.append([sublist[i] for sublist in my_list])
    return (result_list)


SUPERGAME_1 = random_numbers_until()
SUPERGAME_2 = random_numbers_until()
SUPERGAME_3 = random_numbers_until()
SUPERGAME_4 = random_numbers_until()
# Creating 4 sequences for block randomisation

print(SUPERGAME_1, SUPERGAME_2, SUPERGAME_3, SUPERGAME_4)


class C(BaseConstants):
    NAME_IN_URL = 'supergames'
    PLAYERS_PER_GROUP = 2
    MIN_ROUNDS = NUMBER_ROS
    ROUNDS_PER_SG = [max(MIN_ROUNDS, len(SUPERGAME_1)), max(MIN_ROUNDS, len(SUPERGAME_2)),
                     max(MIN_ROUNDS, len(SUPERGAME_3)), max(MIN_ROUNDS, len(SUPERGAME_4))]
    # In the ROUNDS_PER_SG each supergame consist of at least MIN_ROUNDS rounds. If there are less rounds in the supergame, then only those up to the len(supergame) would be payoff-relevant
    SG_ENDS = cumsum(ROUNDS_PER_SG)
    SG_STARTS = calculate_game_starts(ROUNDS_PER_SG)
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
    PER_PERIOD_CONTRACTS = return_lists(POSSIBLE_CONTRACT_ALLOCATIONS)
    SG_1_MATCHING = [[1, 3], [2, 5], [4, 6], [7, 8], [9, 11], [10, 13], [12, 14], [15, 16]]
    SG_2_MATCHING = [[1, 7], [2, 4], [3, 8], [5, 6], [9, 15], [10, 12], [11, 16], [13, 14]]
    SG_3_MATCHING = [[1, 8], [2, 6], [3, 4], [5, 7], [9, 16], [10, 14], [11, 12], [13, 15]]
    SG_4_MATCHING = [[1, 2], [3, 5], [4, 7], [6, 8], [9, 10], [11, 13], [12, 15], [14, 16]]
    LIST_OF_MATCHING_MATRICES = [SG_1_MATCHING, SG_2_MATCHING, SG_3_MATCHING, SG_4_MATCHING]
    ITERATED_LIST_OF_MATCHING_MATRICES = itertools.cycle(LIST_OF_MATCHING_MATRICES)
    POSSIBLE_CONTRACT_ORDERS_THROUGH_ALL_SUPERGAMES = repeat_elements_in_sublists(POSSIBLE_CONTRACT_ALLOCATIONS,
                                                                                  ROUNDS_PER_SG)
    ITERATED_POSSIBLE_CONTRACT_ORDERS_THROUGH_ALL_SUPERGAMES = itertools.cycle(
        POSSIBLE_CONTRACT_ORDERS_THROUGH_ALL_SUPERGAMES)
    ITERATED_CONTRACT_ORDERS = itertools.cycle(POSSIBLE_CONTRACT_ALLOCATIONS)
    # Logic: There are 8 possible orders of how the contracts can be allocated for each supergame. "Repeat elements in the sublist" function then duplicates each contract according to how many rounds are played in a particular supergame.
    # We then assign this list to a participant. When we need to know which contract he is playing in round i, we just call this list[i].
    # The next step is to organise the groups and then reshuffle them for each supergame
    TOTAL_CAPACITY = 100
    MAX_UNITS_PER_PLAYER = int(TOTAL_CAPACITY / 2)
    GAMMA = 1
    #The above are constants for market environment

class Subsession(BaseSubsession):  # Creating fields in the subsession class
    sg = models.IntegerField()
    period = models.IntegerField()
    is_last_period = models.BooleanField()


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():  # I am not sure this thing here is needed - it slows down the session creation since it iterates over (all rounds x all players)
            player.participant.CONTRACT_ORDER = next(C.ITERATED_CONTRACT_ORDERS)
            player.participant.CONTRACTUAL_ORDER_FOR_THIS_PLAYER = next(
                C.ITERATED_POSSIBLE_CONTRACT_ORDERS_THROUGH_ALL_SUPERGAMES)
            player.participant.CONTRACTUAL_ORDER_FOR_THIS_PLAYER_CONTRACT_TYPE = itertools.cycle(
                player.participant.CONTRACTUAL_ORDER_FOR_THIS_PLAYER)
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
    if subsession.round_number in C.SG_STARTS:
        subsession.set_group_matrix(next(C.ITERATED_LIST_OF_MATCHING_MATRICES))
    else:
        subsession.group_like_round(subsession.round_number - 1)
    for player in subsession.get_players():
        # Assigning each player
        player.ORDER = ", ".join(player.participant.CONTRACT_ORDER)
        player.CONTRACT_TYPE_RP = True if (
                    next(player.participant.CONTRACTUAL_ORDER_FOR_THIS_PLAYER_CONTRACT_TYPE)[0] == "R") else False


class Group(BaseGroup):
    UNIT_PRICE = models.CurrencyField()
    TOTAL_UNITS = models.IntegerField(doc="""Total units produced by all players""")


class Player(BasePlayer):
    ORDER = models.StringField()
    CONTRACT_TYPE_RP = models.BooleanField()
    UNITS = models.IntegerField(
        min=0,
        max=C.MAX_UNITS_PER_PLAYER,
        doc="""Quantity of units to produce""",
        label="How many units will you produce (from 0 to 50)?",
    )
    FIRM_PROFITS = models.CurrencyField()
    CHOICE_IN_ROUNDS = models.IntegerField(initial=0)


# FUNCTIONS:

def calculate_payoffs(group: Group):
    players = group.get_players()
    group.TOTAL_UNITS = sum([p.UNITS for p in players])
    group.UNIT_PRICE = C.TOTAL_CAPACITY - group.TOTAL_UNITS
    print()
    for p in players:
        print(p.CONTRACT_TYPE_RP)
        p.FIRM_PROFITS = group.UNIT_PRICE * p.UNITS
        if p.CONTRACT_TYPE_RP == False:
            p.payoff = p.FIRM_PROFITS
        if p.CONTRACT_TYPE_RP == True:
            p.payoff = group.UNIT_PRICE * p.UNITS * (1 + C.GAMMA) - group.UNIT_PRICE * C.GAMMA * (
                        group.TOTAL_UNITS - p.UNITS)
        p.CHOICE_IN_ROUNDS = p.UNITS


def calculate_profits_and_compensation(list_my_choices, list_other_choices, my_contract):
    profits_and_compensation = []
    for period in range(0, len(list_my_choices)):
        price = C.TOTAL_CAPACITY - list_my_choices[period] - list_other_choices[period]
        my_profit = price * list_my_choices[period]
        other_profit = price * list_other_choices[period]
        my_compensation = my_profit
        if my_contract == True:
            my_compensation = (1 + C.GAMMA) * my_profit - C.GAMMA * other_profit
        profits_and_compensation.append([list_my_choices[period], list_other_choices[period], my_profit, other_profit, my_compensation])
    return profits_and_compensation


def other_player(player: Player):
    return player.get_others_in_group()[0]


def get_actions_in_previous_rounds_in_SG(player: Player):
    xx = player.in_previous_rounds()
    previous_actions = []
    for round in xx:
        action = round.UNITS
        previous_actions.append(action)
    return (previous_actions[(C.SG_STARTS[player.subsession.sg - 1] - 1):(
                C.SG_STARTS[player.subsession.sg - 1] - 1 + player.subsession.period)])


# PAGES:
class NewSupergame(Page):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.period == 1


class Play(Page):
    form_model = 'player'
    form_fields = ['UNITS']

    @staticmethod
    def vars_for_template(player: Player):
        if player.subsession.period > 1:
            print("subsession:", player.subsession.sg, "Subsession Starts", C.SG_STARTS[player.subsession.sg - 1])
            my_actions = get_actions_in_previous_rounds_in_SG(player)
            other_actions = get_actions_in_previous_rounds_in_SG(other_player(player))
            table_to_display = calculate_profits_and_compensation(my_actions, other_actions, player.CONTRACT_TYPE_RP)
            print(table_to_display)
            print("my actions", my_actions)
            print("other_actions", other_actions)
        else:
            table_to_display=[]
            # print(xx[0])
            # print(player.in_previous_rounds())

        return dict(table_to_display=table_to_display)
    # The vars for template function creates variables that can be used in the play.html and "newSupergame".
    # After period 1 in each supergame, we would display the history of previous plays which include my_action (a list of periods from 1 to current period),
    # Others_action( a list of periods from 1 to current period) and "table_to_display" which is a list of lists of the type [profit of my firm, profit of the other firm, my compensation]
    # Ideally the play page would contain a function that generates a new row in a list depending on the length of either table
    # After that we can add a calculator and define the payment mechanism


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for the other participant to decide."
    after_all_players_arrive = calculate_payoffs


page_sequence = [NewSupergame, Play, ResultsWaitPage]
