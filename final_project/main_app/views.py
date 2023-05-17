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
        income_statement = IncomeStatement.objects.filter(company=self.kwargs["pk"]).order_by("year")
        balance_sheet = BalanceSheet.objects.filter(company=self.kwargs["pk"]).order_by("year")
        cash_flow_statement = CashFlowStatement.objects.filter(company=self.kwargs["pk"]).order_by("year")
        context["income_statement"] = income_statement
        context["balance_sheet"] = balance_sheet
        context["cash_flow_statement"] = cash_flow_statement
        return context
