from otree.api import *
import secrets
import string
from settings import LANGUAGE_CODE
import random


doc = """
A simple 1-round ultimatum game
"""

class Constants(BaseConstants):
    name_in_url = 'pb'
    num_rounds = 1
    players_per_group = 4
    INITIAL_ENDOWMENT = 20
    MULTIPLIER = 0.4


class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0,
        max=Constants.INITIAL_ENDOWMENT
    )

    def contribution_error_message(player, value):
        if value > Constants.INITIAL_ENDOWMENT:
            return 'Cannot contribute more than your initial endowment'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def creating_session(subsession: Subsession):
    pass

def set_payoffs(group: Group):
    pass

# FUNCTIONS


def set_payoffs(group):
    total_contribution = sum(p.contribution for p in group.get_players())
    for p in group.get_players():
        p.payoff = (Constants.INITIAL_ENDOWMENT - p.contribution) + (
            Constants.MULTIPLIER * total_contribution
        )

# PAGES

class GroupWaitPage(WaitPage):
    group_by_arrival_time = True

class PublicGoodPage(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def vars_for_template(player: Player):

        return {
            'player_role': player.role,
            'initial_endowment': Constants.INITIAL_ENDOWMENT,
        }

class WaitForContributionsPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)

class ResultPage(Page):
    pass








page_sequence = [GroupWaitPage, PublicGoodPage, WaitForContributionsPage, ResultPage]
