from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from main_app.models import Company


class HomeView(View):
    def get(self, request):
        companies = Company.objects.order_by("-market_cap")[:10]
        return render(request, "home.html", context={
            "companies": companies
        })


class CompaniesListView(ListView):
    model = Company
    paginate_by = 5


class CompanyDetailsView(View):
    def get(self, request, company_id):
        return render(request, "company_details.html")
