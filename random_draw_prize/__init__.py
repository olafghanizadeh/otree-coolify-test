from otree.api import *
from settings import LANGUAGE_CODE
import random


doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""



class Constants(BaseConstants):
    name_in_url = 'random_draw_prize'
    num_rounds = 1
    players_per_group = None


class Player(BasePlayer):
    pass


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def creating_session(subsession: Subsession):
    session = subsession.session
    session.vars['draw_done'] = False
    session.vars['drawn_winners_codes'] = []
    session.vars['eligible_codes'] = []
    session.vars['draw_reason'] = ''

# FUNCTIONS


# PAGES


def vars_for_admin_report(subsession: Subsession):
    s = subsession.session
    all_codes = [p.participant.code for p in subsession.get_players()]

    return dict(
        total_players=len(all_codes),
        winners=s.vars.get('drawn_winners_codes', []),
        reason=s.vars.get('draw_reason', ''),
    )


def run_draw(subsession: Subsession):
    session = subsession.session
    if session.vars['draw_done']:
        return

    n = int(session.config['number_of_winners'])


    # Eligible = reached this app (flag set on arrival page) AND not fast-forwarded earlier
    players = subsession.get_players()
    eligible = [
        p for p in players
        if p.participant.vars.get('arrived_at_draw', False)
        and not p.participant.vars.get('advanced_by_timeout', False)
    ]

    if n <= 0 or not eligible:
        session.vars['draw_done'] = True
        session.vars['drawn_winners_codes'] = []
        session.vars['eligible_codes'] = [p.participant.code for p in eligible]
        session.vars['draw_reason'] = 'no_eligible_or_zero_n'
        return

    winners = random.sample(eligible, k=min(n, len(eligible)))
    
    session.vars['draw_done'] = True
    session.vars['drawn_winners_codes'] = [w.participant.code for w in winners]
    session.vars['eligible_codes'] = [p.participant.code for p in eligible]
    session.vars['draw_reason'] = 'ok'


class WaitForDrawPage(WaitPage):
    wait_for_all_groups = True
    
    @staticmethod
    def is_displayed(player: Player):
        # Mark that this participant actually reached the prize app.
        player.participant.vars['arrived_at_draw'] = True
        return True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        run_draw(subsession)

    @staticmethod
    def after_timeout(subsession: Subsession):
        run_draw(subsession)


class PaymentInfo(Page):

    def vars_for_template(player: Player):
        winners = player.session.vars['drawn_winners_codes']
        return dict(
            participant_id=player.participant.code,
            winners=winners,
            is_winner=player.participant.code in winners
        )


page_sequence = [WaitForDrawPage, PaymentInfo]
