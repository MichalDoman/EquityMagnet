from django.shortcuts import render
from django.views import View

from main_app.models import Company


class HomeView(View):
    def get(self, request):
        companies = Company.objects.order_by("-market_cap")[:10]
        return render(request, "home.html", context={
            "companies": companies
        })


class CompaniesListView(View):
    def get(self, request, stock_market):
        return render(request, "companies.html")


class CompanyDetailsView(View):
    def get(self, request, company_id):
        return render(request, "company_details.html")
