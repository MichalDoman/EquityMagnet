from django import forms
from django.core.validators import MinValueValidator

from main_app.models import Exchange, Sector
from main_app.utils import get_all_countries


class SearchFiltersForm(forms.Form):
    phrase = forms.CharField(max_length=64, required=False)
    exchanges = forms.MultipleChoiceField(required=False)
    sectors = forms.MultipleChoiceField(required=False)
    countries = forms.MultipleChoiceField(required=False)
    market_cap = forms.IntegerField(validators=[MinValueValidator(0)], required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['exchanges'].choices = self.get_exchange_choices()
        self.fields['sectors'].choices = self.get_sector_choices()
        self.fields['countries'].choices = self.get_country_choices()

    @staticmethod
    def get_exchange_choices():
        return [(exchange.pk, exchange.symbol) for exchange in Exchange.objects.all()]

    @staticmethod
    def get_sector_choices():
        return [(sector.pk, sector.name) for sector in Sector.objects.all()]

    @staticmethod
    def get_country_choices():
        choices = []
        for num, country in enumerate(get_all_countries()):
            choices.append((num, country))
        return choices


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=256)
    last_name = forms.CharField(max_length=256)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeated = forms.CharField(widget=forms.PasswordInput)

# class EvaluationEditablesForm(forms.Form):
#     wacc =
#     g =
#     average_revenue =
#     koszty_w_przychodach =
#     dynamika_aktywow=
#     dynamika_pasywów =
#     podatek =
#     udział_pozostałych_kosztów =
#     instrukcja do wyceny
