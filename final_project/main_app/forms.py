from django import forms
from django.core.validators import MinValueValidator

from main_app.models import Exchange, Sector, Company


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
        country_set = set()
        for company in Company.objects.all():
            country_set.add(company.country)

        choices = []
        for num, country in enumerate(list(country_set)):
            choices.append((num, country))
        return choices
