from otree.api import *
from settings import LANGUAGE_CODE


doc = """
A simple 1-round loss aversion game
"""



from otree.api import *

# ---------- data ----------
LAS_CHOICES = [
    [1, 'Completamente em desacordo'],
    [2, 'Em desacordo'],
    [3, 'Nem de acordo nem em desacordo'],
    [4, 'De acordo'],
    [5, 'Completamente de acordo'],
]

LAS_LABELS = [
    "Quando tomo uma decisão, penso muito mais no que posso perder do que no que posso ganhar",
    "A angústia de perder dinheiro tem mais importância do que o prazer de ganhar a mesma quantia",
    "Fico nervoso quando tenho de tomar uma decisão que pode levar a uma perda",
    "Para mim, a angústia de perder algo tem mais importância do que o prazer de o conseguir",
    "Para mim, evitar o fracasso é menos importante do que perseguir o sucesso",
    "Experienciar uma grande perda permanece mais tempo na memória do que experienciar um grande ganho",
    "Tenho mais medo de um possível fracasso do que motivação por uma possível conquista",
    "O sofrimento que vem com as perdas pode ser totalmente compensado pelo prazer que vem com os ganhos",
]

# ---------- core ----------
class Constants(BaseConstants):
    name_in_url = 'las_textual'
    players_per_group = None
    num_rounds = 1


class Player(BasePlayer):
    # Generate LAS_1 ... LAS_n as IntegerFields
    for i, lab in enumerate(LAS_LABELS, start=1):
        locals()[f'LAS_{i}'] = models.IntegerField(
            choices=LAS_CHOICES,
            widget=widgets.RadioSelect,
            label=lab,
        )
    del i, lab


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def creating_session(subsession: Subsession):
    pass


# Create named Page classes and register them in globals()
for i, lab in enumerate(LAS_LABELS, start=1):
    field_name = f'LAS_{i}'
    cls_name = f'LAS_{i}'

    def _vft(player, field_name=field_name, lab=lab):
        return dict(field_name=field_name, label=lab)

    cls = type(
        cls_name,
        (Page,),
        dict(
            form_model='player',
            form_fields=[field_name],
            template_name='las_textual/Question.html',
            vars_for_template=_vft,
        ),
    )

    # register the class so it's available in globals()
    globals()[cls_name] = cls

# now this works because LAS_1, LAS_2, ... exist in globals
page_sequence = [globals()[f'LAS_{i}'] for i in range(1, len(LAS_LABELS) + 1)]
PAGE_NAMES = [cls.__name__ for cls in page_sequence]