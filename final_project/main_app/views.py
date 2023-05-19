from random import sample
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from main_app.models import Company, IncomeStatement, BalanceSheet, CashFlowStatement
from main_app.utils import get_field_dictionaries, style_numeric_data


class HomeView(View):
    """A view supporting GET method, that represents the Home Page of the app.

    :return: an HTTPResponse that passes a context to the home.html template.
    The context contain a list of tuples. These tuples are constructed from Company objects,
    and their styled, market cap values.
    """
    def get(self, request):
        all_companies = Company.objects.all()
        sample_companies = sample(list(all_companies), 1)
        company_tuples = []
        for company in sample_companies:
            market_cap = style_numeric_data([company.market_cap])[0]
            company_tuples.append((company, market_cap))

        return render(request, "home.html", context={
            "company_tuples": company_tuples
        })


class CompaniesListView(ListView):
    """A generic list view for Company objects"""
    model = Company
    paginate_by = 5


class CompanyDetailView(DetailView):
    model = Company
    context_object_name = "company"

    def get_context_data(self, **kwargs):
        """Extend context by company's financial statements and all of their field names"""

        context = super().get_context_data(**kwargs)

        market_cap = Company.objects.get(id=self.kwargs["pk"]).market_cap
        context["market_cap"] = style_numeric_data([market_cap])

        income_statements = IncomeStatement.objects.filter(company=self.kwargs["pk"]).order_by("year")
        balance_sheets = BalanceSheet.objects.filter(company=self.kwargs["pk"]).order_by("year")
        cash_flow_statements = CashFlowStatement.objects.filter(company=self.kwargs["pk"]).order_by("year")

        # Add all field names of every type of statement to the context:
        context["income_statement_dicts"] = get_field_dictionaries(income_statements)
        context["balance_sheet_dicts"] = get_field_dictionaries(balance_sheets)
        context["cash_flow_statement_dicts"] = get_field_dictionaries(cash_flow_statements)
        return context



