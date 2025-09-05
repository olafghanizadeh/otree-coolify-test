from otree.api import *
import secrets
import string
from settings import LANGUAGE_CODE
import random


doc = """
A simple 1-round ultimatum game
"""

class Constants(BaseConstants):
    name_in_url = 'ultimatum'
    num_rounds = 1
    players_per_group = 2
    RESPONDER_ROLE = 'Responder'
    PROPOSER_ROLE = 'Proposer'
    INITIAL_ENDOWMENT = 100


class Player(BasePlayer):
    proposer_offer = models.IntegerField(
        min=0,
        max=Constants.INITIAL_ENDOWMENT
    )
    responder_accept = models.BooleanField()

    def proposer_offer_error_message(player, value):
        if value > Constants.INITIAL_ENDOWMENT:
            return 'Cannot offer more than your initial endowment'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def creating_session(subsession: Subsession):
    pass

def set_payoffs(group: Group):
    proposer = group.get_player_by_role(Constants.PROPOSER_ROLE)
    responder = group.get_player_by_role(Constants.RESPONDER_ROLE)

    if responder.responder_accept:
        proposer.payoff = Constants.INITIAL_ENDOWMENT - proposer.proposer_offer
        responder.payoff = proposer.proposer_offer
    else:
        proposer.payoff = 0
        responder.payoff = 0


# FUNCTIONS
# PAGES

class GroupWaitPage(WaitPage):
    group_by_arrival_time = True


class UltimatumPage(Page):
    form_model = 'player'
    form_fields = ['proposer_offer']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.PROPOSER_ROLE

    @staticmethod
    def vars_for_template(player: Player):

        return {
            'player_role': player.role,
            'initial_endowment': Constants.INITIAL_ENDOWMENT,
        }

class WaitForProposerPage(WaitPage):

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.RESPONDER_ROLE

class ResponsePage(Page):
    form_model = 'player'
    form_fields = ['responder_accept']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.RESPONDER_ROLE

    @staticmethod
    def vars_for_template(player: Player):
        partner = player.get_others_in_group()[0]
        return {
            'proposer_offer': partner.proposer_offer,
            'initial_endowment': Constants.INITIAL_ENDOWMENT,
        }

class WaitForResponder(WaitPage):

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.PROPOSER_ROLE



page_sequence = [GroupWaitPage, UltimatumPage, WaitForProposerPage,  ResponsePage, WaitForResponder]
