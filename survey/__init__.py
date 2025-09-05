from otree.api import *
import requests
from gettext import gettext
from settings import LANGUAGE_CODE

class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='Em que ano nasceste?', min=1960, max=2020)
    gender = models.StringField(
        choices=[[0, 'Masculino'], [1, 'Feminino'], [2, 'Outro/Prefiro não divulgar']],
        label='Qual é o seu género?',
    )    
    programme = models.StringField(
        label="Que curso está a realizar no ISEG?",
        choices=[
            'Economia',
            'Economics',
            'Finance',
            'Gestão',
            'MAEG',
            'Management'
        ]
    )
    postal = models.StringField(
        label="Qual é o teu código postal?"
    )

# FUNCTIONS
# PAGES

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'programme', 'postal']

page_sequence = [Demographics]
