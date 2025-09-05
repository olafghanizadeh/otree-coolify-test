from otree.api import *
import secrets
import string
from settings import LANGUAGE_CODE
import random


doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


def generate_code():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(6))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break

    return password

class Constants(BaseConstants):
    name_in_url = 'payment_info'
    num_rounds = 1
    players_per_group = None


class Player(BasePlayer):
    redemption_code = models.StringField()


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def creating_session(subsession: Subsession):
    for player in subsession.get_players():
        player.redemption_code = generate_code()


# FUNCTIONS
# PAGES
class PaymentInfo(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'participant_id': participant.code,
            'redemption_code': player.redemption_code,
            'lang': LANGUAGE_CODE
        }

page_sequence = [PaymentInfo]
