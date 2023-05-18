from random import sample
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from main_app.models import Company, IncomeStatement, BalanceSheet, CashFlowStatement


class HomeView(View):
    def get(self, request):
        all_companies = Company.objects.all()
        sample_companies = sample(list(all_companies), 4)
        return render(request, "home.html", context={
            "companies": sample_companies
        })


class CompaniesListView(ListView):
    model = Company
    paginate_by = 5


class CompanyDetailView(DetailView):
    model = Company
    context_object_name = "company"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        income_statements = IncomeStatement.objects.filter(company=self.kwargs["pk"]).order_by("year")
        balance_sheets = BalanceSheet.objects.filter(company=self.kwargs["pk"]).order_by("year")
        cash_flow_statements = CashFlowStatement.objects.filter(company=self.kwargs["pk"]).order_by("year")
        # Add all statements for all years for a given company to the context:
        context["income_statements"] = income_statements
        context["balance_sheets"] = balance_sheets
        context["cash_flow_statements"] = cash_flow_statements
        # Add all field names of every type of statement to the context:
        context["income_statement_fields"] = get_statement_fields_names(income_statements[0])
        context["balance_sheet_fields"] = get_statement_fields_names(balance_sheets[0])
        context["cash_flow_statement_fields"] = get_statement_fields_names(cash_flow_statements[0])
        return context


def get_statement_fields_names(instance):
    """Capitalize and space all the field names of a given financial statement model.

    :param instance: An instance of a model of one of the financial statements.
    :return: A list of capitalized and properly spaced field names of a given statement.
    The list excludes company and year fields.
    """

    field_names = [field.name for field in instance._meta.get_fields()]
    styled_field_names = []
    for name in field_names:
        name = name.capitalize()
        name = name.replace("_", " ")
        styled_field_names.append(name)
    return styled_field_names[3:]
