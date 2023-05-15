from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class CompaniesListView(View):
    def get(self, request, stock_market):
        return render(request, "companies.html")


class CompanyDetailsView(View):
    def get(self, request, company_id):
        return render(request, "company_details.html")
