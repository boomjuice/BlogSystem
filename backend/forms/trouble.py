from django.forms import Form
from django.forms import fields
from django.forms import widgets
from repository.models import *


class TroubleAddForm(Form):
    title = fields.CharField(
        max_length=32,
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'add-trouble'})
    )


class TroubleSolution(Form):
    solution = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'solution'})
    )


class SolutionEvaluate(Form):
    evaluate = fields.IntegerField(
        widget=widgets.RadioSelect(choices=Trouble.evaluate_choices)
    )