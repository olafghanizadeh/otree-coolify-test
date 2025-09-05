import random
import numpy as np
from otree.api import *
from gettext import gettext
from settings import LANGUAGE_CODE

# Moved index function to separate file to keep this file cleaner

author = 'Olaf Ghanizadeh'
doc = """
A crude and simple implementation of the Holt/Laury(2002) lottery.
"""

class Constants(BaseConstants):
    name_in_url = 'loss_aversion'
    players_per_group = None
    num_rounds = 1


class Player(BasePlayer):
    """The oTree class that generates the info PER PLAYER"""
    input = models.IntegerField()


class Subsession(BaseSubsession):
    """Creating the lottery subsessions"""


class Group(BaseGroup):
    pass


# FUNCTIONS
# Class for the DecisionPage. Inherits attributes from Page Class
class InputPage(Page):
    form_model = 'player'
    form_fields = ['input']

# The sequence the app will order the pages.
page_sequence = [InputPage]
