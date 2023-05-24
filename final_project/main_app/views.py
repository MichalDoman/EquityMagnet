import json
from random import sample

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView

from main_app.models import Company, IncomeStatement, BalanceSheet, CashFlowStatement, Price, FavoriteCompany
from main_app.utils import get_field_dictionaries, extract_historical_prices


class HomeView(View):
    """A view supporting GET method, that represents the Home Page of the app.

    :return: an HTTPResponse that passes a context to the home.html template.
    The context contain a random sample of companies from database.
    """

    def get(self, request):
        all_companies = Company.objects.all()
        sample_companies = sample(list(all_companies), 4)

        return render(request, "home.html", context={
            "companies": sample_companies
        })


class CompanyListView(ListView, LoginRequiredMixin):
    """A generic list view for Company objects"""
    model = Company
    paginate_by = 10


class CompanyDetailView(DetailView):
    model = Company
    context_object_name = "company"

    def get_context_data(self, **kwargs):
        """Extend context by company's financial statements and all of their field names"""

        context = super().get_context_data(**kwargs)

        income_statements = IncomeStatement.objects.filter(company=self.kwargs["pk"]).order_by("year")
        balance_sheets = BalanceSheet.objects.filter(company=self.kwargs["pk"]).order_by("year")
        cash_flow_statements = CashFlowStatement.objects.filter(company=self.kwargs["pk"]).order_by("year")

        # Add all field names of every type of statement to the context:
        context["income_statement_dicts"] = get_field_dictionaries(income_statements)
        context["balance_sheet_dicts"] = get_field_dictionaries(balance_sheets)
        context["cash_flow_statement_dicts"] = get_field_dictionaries(cash_flow_statements)

        # Add company's historical data to the context:
        price = Price.objects.get(company=self.kwargs["pk"])
        history = price.history['historical']
        dates, historical_prices = extract_historical_prices(history)

        context["chart_labels"] = json.dumps(dates)
        context["chart_data"] = json.dumps(historical_prices)
        return context


class ManageFavoritesView(View, LoginRequiredMixin):
    def post(self, request):
        response = {"is_authenticated": request.user.is_authenticated}
        if response['is_authenticated']:
            company_id = request.POST["company_id"][0]
            company = Company.objects.get(pk=company_id)

            is_favorite = FavoriteCompany.objects.filter(user=request.user, company=company).exists()
            if is_favorite:
                FavoriteCompany.objects.get(user=request.user, company=company).delete()
                messages.add_message(request, messages.SUCCESS, f"{company.symbol} was removed from favorites.")
            else:
                FavoriteCompany.objects.create(user=request.user, company=company)
                messages.add_message(request, messages.SUCCESS, f"{company.symbol} was added to favorites.")

            response["is_favorite"] = is_favorite
            return JsonResponse(response)

        return JsonResponse(response)


class CustomLogoutView(LogoutView):
    pass
