from random import sample
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from main_app.models import Company, IncomeStatement, BalanceSheet, CashFlowStatement


class HomeView(View):
    def get(self, request):
        all_companies = Company.objects.all()
        sample_companies = sample(list(all_companies), 1)
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
        """Extend context by company's financial statements and all of their field names"""

        context = super().get_context_data(**kwargs)
        income_statements = IncomeStatement.objects.filter(company=self.kwargs["pk"]).order_by("year")
        balance_sheets = BalanceSheet.objects.filter(company=self.kwargs["pk"]).order_by("year")
        cash_flow_statements = CashFlowStatement.objects.filter(company=self.kwargs["pk"]).order_by("year")

        # Add all statements for all years for a given company to the context:
        context["income_statements"] = income_statements
        context["balance_sheets"] = balance_sheets
        context["cash_flow_statements"] = cash_flow_statements

        # Add all field names of every type of statement to the context:
        context["income_statement_dicts"] = get_field_dictionaries(income_statements)
        context["balance_sheet_dicts"] = get_field_dictionaries(balance_sheets)
        context["cash_flow_statement_dicts"] = get_field_dictionaries(cash_flow_statements)
        return context


def get_field_dictionaries(queryset):
    field_names = [field.name for field in queryset[0]._meta.get_fields()]
    field_dictionaries = []

    for field_name in field_names:
        values = []

        for instance in queryset:
            value = getattr(instance, field_name)
            values.append(value)
        styled_name = field_name.capitalize().replace("_", " ")
        field_dictionaries.append({styled_name: values})
    return field_dictionaries[2:]
