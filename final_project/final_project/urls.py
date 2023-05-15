from django.contrib import admin
from django.urls import path
from main_app.views import HomeView, CompaniesListView, CompanyDetailsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("companies/<str:stock_market>", CompaniesListView.as_view(), name="companies"),
    path("company-details/<int:company_id>", CompanyDetailsView.as_view(), name="company_details"),
]
