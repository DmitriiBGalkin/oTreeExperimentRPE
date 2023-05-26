from otree.api import *
import random
import itertools
from settings import LANGUAGE_CODE
if LANGUAGE_CODE == 'de':
    from .lexicon_de import Lexicon
else:
    from .lexicon_en import Lexicon
which_language = {'en': False, 'de': False}  # noqa
which_language[LANGUAGE_CODE[:2]] = True
doc = """   
Cournot Supergames
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


# The above function repeats the strings

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
    return result_list


SUPERGAME_1 = random_numbers_until()
SUPERGAME_2 = random_numbers_until()
SUPERGAME_3 = random_numbers_until()
SUPERGAME_4 = random_numbers_until()
# Creating 4 sequences for block randomisation
#print(SUPERGAME_1, SUPERGAME_2, SUPERGAME_3, SUPERGAME_4)


class C(BaseConstants):
    NAME_IN_URL = 'ExperimentalStudyOfContracts'
    PLAYERS_PER_GROUP = 2
    MIN_ROUNDS = NUMBER_ROS
    RANDOM_SEQUENCE_IN_SUPERGAMES = [SUPERGAME_1, SUPERGAME_2, SUPERGAME_3, SUPERGAME_4]
    ROUNDS_PER_SG = [max(MIN_ROUNDS, len(SUPERGAME_1)), max(MIN_ROUNDS, len(SUPERGAME_2)),
                     max(MIN_ROUNDS, len(SUPERGAME_3)), max(MIN_ROUNDS, len(SUPERGAME_4))]
    # In the ROUNDS_PER_SG each supergame consist of at least MIN_ROUNDS rounds.
    # If there are less rounds in the supergame then only those up to the len(supergame) would be payoff-relevant
    SG_ENDS = cumsum(ROUNDS_PER_SG)
    SG_STARTS = calculate_game_starts(ROUNDS_PER_SG)
    #print('SG_ENDS is', SG_ENDS)
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
    # Logic: There are 8 possible orders of how the contracts can be allocated for each supergame.
    # "Repeat elements in the sublist" function then duplicates each contract according to how many rounds are played in a particular supergame.
    # We then assign this list to a participant. When we need to know which contract he is playing in round i, we just call this list[i].
    # The next step is to organise the groups and then reshuffle them for each supergame
    TOTAL_CAPACITY = 100
    MAX_UNITS_PER_PLAYER = 70
    GAMMA = 1
    BONUS_FIXED = 100
    # The above are constants for market environment
    CORRECT_ANSWERS = {
        'q1': 1350,
        'q2': 44,
        'q3': 1222
    }
    EXCHANGE_RATE = 1000
    CHAT_LENGTH_ONE = 180


class Subsession(BaseSubsession):
    # Creating fields in the subsession class
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
            player.WHICH_SUPERGAME = random.randint(0, 3)
        sg = 1
        period = 1
        print(C.NUM_ROUNDS)
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
    UNIT_PRICE = models.IntegerField()
    TOTAL_UNITS = models.IntegerField(doc="""Total units produced by all players""")


class Player(BasePlayer):
    ORDER = models.StringField()
    CONTRACT_TYPE_RP = models.BooleanField()
    UNITS = models.IntegerField(
        min=0,
        max=C.MAX_UNITS_PER_PLAYER,
        doc="""Quantity of units to produce""",
        label=Lexicon.player_choice_label,
    )
    FIRM_PROFITS = models.IntegerField()
    CHOICE_IN_ROUNDS = models.IntegerField(initial=0)
    COMPENSATION = models.IntegerField()
    WHICH_SUPERGAME = models.IntegerField()
    q1 = models.IntegerField(
        min=0,
        max=5000,
        doc="COMPREHENSION QUESTION 1",
        label=Lexicon.comprehension_question_1,

    )
    q2 = models.IntegerField(
        min=0,
        max=C.MAX_UNITS_PER_PLAYER,
        doc="COMPREHENSION QUESTION 1",
        label=Lexicon.comprehension_question_2,

    )
    q3 = models.IntegerField(
        min=0,
        max=5000,
        doc="COMPREHENSION QUESTION 1",
        label=Lexicon.comprehension_question_3,

    )
    #for code in the Uni Wuppertal:
    codeU1_firstletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU1_secondletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU1_penletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU1_lastletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU2_birthday = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    )
    codeU3_firstletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU3_secondletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU4_firstletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU4_secondletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU4_penletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU4_lastletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU5_birthday = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                 29, 30, 31]
    )
    codeU6_birthday = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                 29, 30, 31]
    )
    codeU7_firstletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU7_secondletter = models.StringField(
        choices=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z']
    )
    codeU8_siblings = models.BooleanField()
    codeU9_order = models.StringField()


class Message(ExtraModel):
    group = models.Link(Group)
    sender = models.Link(Player)
    text = models.StringField()


def to_dict(msg: Message):
    return dict(sender=msg.sender.id_in_group, text=msg.text)

# FUNCTIONS:


def calculate_payoffs(group: Group):
    players = group.get_players()
    group.TOTAL_UNITS = sum([p.UNITS for p in players])
    group.UNIT_PRICE = C.TOTAL_CAPACITY - group.TOTAL_UNITS
    for p in players:
        p.FIRM_PROFITS = group.UNIT_PRICE * p.UNITS
        if not p.CONTRACT_TYPE_RP:
            p.COMPENSATION = p.FIRM_PROFITS + C.BONUS_FIXED
        if p.CONTRACT_TYPE_RP:
            p.COMPENSATION = max(0, group.UNIT_PRICE * p.UNITS * (1 + C.GAMMA) - group.UNIT_PRICE * C.GAMMA * (
                        group.TOTAL_UNITS - p.UNITS) + C.BONUS_FIXED)
        p.CHOICE_IN_ROUNDS = p.UNITS


def calculate_profits_and_compensation(list_my_choices, list_other_choices, my_contract):
    profits_and_compensation = []
    for period in range(0, len(list_my_choices)):
        price = C.TOTAL_CAPACITY - list_my_choices[period] - list_other_choices[period]
        my_profit = price * list_my_choices[period]
        other_profit = price * list_other_choices[period]
        my_compensation = my_profit + C.BONUS_FIXED
        if my_contract:
            my_compensation = max(0, C.BONUS_FIXED + (1 + C.GAMMA) * my_profit - C.GAMMA * other_profit)
        profits_and_compensation.append(
            [list_my_choices[period], list_other_choices[period], my_profit, other_profit, my_compensation])
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

def set_final_payoffs(player: Player):
    PAYOFF_RELEVANT_SUPERGAME = player.in_round(1).WHICH_SUPERGAME
    RANDOM_SEQUENCE = C.RANDOM_SEQUENCE_IN_SUPERGAMES[PAYOFF_RELEVANT_SUPERGAME]
    qq = player.in_rounds(C.SG_STARTS[PAYOFF_RELEVANT_SUPERGAME], C.SG_ENDS[PAYOFF_RELEVANT_SUPERGAME])
    table_to_display = []
    subperiod = 0
    for round in qq:
        action = round.field_maybe_none("UNITS")
        profits = round.field_maybe_none("FIRM_PROFITS")
        compensation = round.field_maybe_none("COMPENSATION")
        random_number = RANDOM_SEQUENCE[subperiod] if (subperiod<len(RANDOM_SEQUENCE)) else Lexicon.not_payoff_relevant
        contract = Lexicon.contract_a if (round.CONTRACT_TYPE_RP == False) else Lexicon.contract_b
        subperiod = subperiod + 1
        table_to_display.append([subperiod, action, profits, compensation, random_number, contract])
    return(table_to_display)



# PAGES:


class IntroductionGeneral(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language
        )


class IntroductionMarket(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language
        )



class IntroductionCalculator(Page):

    form_model = 'player'
    form_fields = ['q1', 'q2','q3']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    @staticmethod

    def error_message(player, values):
        if not (values['q1'] == C.CORRECT_ANSWERS['q1'] and values['q2'] == C.CORRECT_ANSWERS['q2'] and values['q3'] == C.CORRECT_ANSWERS['q3']):
            return Lexicon.at_least_one_answer_wrong
    def vars_for_template(player: Player):
        return dict(
            Lexicon=Lexicon,
            **which_language
        )


class IntroductionGame(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    def vars_for_template(player: Player):
        return dict(
            EXCHANGE_RATE = C.EXCHANGE_RATE,
            Lexicon=Lexicon,
            **which_language
            )
    def js_vars(player: Player):
        return dict(
            EXCHANGE_RATE=C.EXCHANGE_RATE,
            is_it_en = which_language['en']
        )

class FirstGame(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    def vars_for_template(player: Player):
        chat_treatment = player.session.config['chat_treatment']
        return dict(
            Lexicon=Lexicon,
            **which_language,
            is_chat = chat_treatment
        )


class NewSupergame(Page):
    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.period == 1

    @staticmethod
    def vars_for_template(player: Player):
        CONTRACT_TYPE = player.CONTRACT_TYPE_RP
        YOUR_CONTRACT = Lexicon.contract_a if (CONTRACT_TYPE == False) else Lexicon.contract_b
        CONTRACT_TYPE_OTHER = other_player(player).CONTRACT_TYPE_RP
        OTHER_CONTRACT = Lexicon.contract_a if (CONTRACT_TYPE_OTHER == False) else Lexicon.contract_b
        chat_treatment = player.session.config['chat_treatment']
        return dict(
            your_contract=YOUR_CONTRACT,
            other_contract=OTHER_CONTRACT,
            Lexicon=Lexicon,
            **which_language,
            is_chat = chat_treatment,
        )
    @staticmethod
    def js_vars(player):
        return dict(
            CONTRACT_RP=player.CONTRACT_TYPE_RP,
            is_it_en=which_language['en'],
            my_id=player.id_in_group
        )
    @staticmethod
    def live_method(player: Player, data):
        my_id = player.id_in_group
        group = player.group
        if 'text' in data:
            text = data['text']
            msg = Message.create(group=group, sender=player, text=text)
            return {0: [to_dict(msg)]}
        return {my_id: [to_dict(msg) for msg in Message.filter(group=group)]}


class Play(Page):
    form_model = 'player'
    form_fields = ['UNITS']
    @staticmethod
    def vars_for_template(player: Player):
        CONTRACT_TYPE = player.CONTRACT_TYPE_RP
        YOUR_CONTRACT = Lexicon.contract_a if (CONTRACT_TYPE == False) else Lexicon.contract_b
        CONTRACT_TYPE_OTHER = other_player(player).CONTRACT_TYPE_RP
        OTHER_CONTRACT = Lexicon.contract_a if (CONTRACT_TYPE_OTHER == False) else Lexicon.contract_b
        if player.subsession.period > 1:
            #print("subsession:", player.subsession.sg, "Subsession Starts", C.SG_STARTS[player.subsession.sg - 1])
            my_actions = get_actions_in_previous_rounds_in_SG(player)
            other_actions = get_actions_in_previous_rounds_in_SG(other_player(player))
            table_to_display = calculate_profits_and_compensation(my_actions, other_actions, CONTRACT_TYPE)
            #print(table_to_display)
            #print("my actions", my_actions)
            #print("other_actions", other_actions)
        else:
            table_to_display = []
            # print(xx[0])
            # print(player.in_previous_rounds())

        return dict(
            table_to_display=table_to_display,
            your_contract=YOUR_CONTRACT,
            other_contract=OTHER_CONTRACT,
            Lexicon=Lexicon,
            **which_language
        )

    @staticmethod
    def js_vars(player):
        return dict(
            CONTRACT_RP=player.CONTRACT_TYPE_RP,
            is_it_en = which_language['en']
        )
    # The vars for template function creates variables that can be used in the play.html and "newSupergame".
    # After period 1 in each supergame, we would display the history of previous plays which include my_action (a list of periods from 1 to current period),
    # Others_action( a list of periods from 1 to current period) and "table_to_display" which is a list of lists of the type [profit of my firm, profit of the other firm, my compensation]
    # Ideally the play page would contain a function that generates a new row in a list depending on the length of either table
    # After that we can add a calculator and define the payment mechanism


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for the other participant to decide." if (which_language['en']) else "Wir warten auf die Entscheidung des anderen Teilnehmers."
    after_all_players_arrive = calculate_payoffs

class WaitForOthers(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        subsession = player.subsession
        return subsession.period == 1
    body_text = "Waiting for the other participant." if (which_language['en']) else "Warten auf die/den andere/n Teilnehmer/in."



class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['codeU1_firstletter', 'codeU1_secondletter', 'codeU1_penletter', 'codeU1_lastletter', 'codeU2_birthday', 'codeU3_firstletter', 'codeU3_secondletter', 'codeU4_firstletter', 'codeU4_secondletter', 'codeU4_penletter', 'codeU4_lastletter', 'codeU5_birthday', 'codeU6_birthday', 'codeU7_firstletter', 'codeU7_secondletter', 'codeU8_siblings', 'codeU9_order']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.session.config['uni_wuppertal']


class FinalResultsPage(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        display_table_final = set_final_payoffs(player)
        valid_rows = [row for row in display_table_final if isinstance(row[4], int) and row[3] is not None]
        cumulative_payment = round( sum(row[3] for row in valid_rows) / C.EXCHANGE_RATE, 2)
        print(cumulative_payment)
        player.payoff = cumulative_payment
        chosen_supergame = player.in_round(1).WHICH_SUPERGAME + 1
        return dict(
            display_table_final = display_table_final,
            your_final_payoff = cumulative_payment,
            chosen_supergame = chosen_supergame,
            total_payment = round(cumulative_payment + 5, 2),
            Lexicon=Lexicon,
            **which_language
        )


page_sequence = [IntroductionGeneral, IntroductionMarket, IntroductionCalculator, IntroductionGame, FirstGame, WaitForOthers, NewSupergame, Play, ResultsWaitPage, Questionnaire, FinalResultsPage]
#Making the chat easier to export

def custom_export(players):
    yield ['session.code', 'round_number', 'player.group', 'player.id_in_subsession', 'message_text']
    messages = Message.filter()
    for message in messages:
        player = message.sender
        group = message.group
        participant = player.participant
        yield[participant.code, player.round_number, group, participant.id_in_session, message.text]