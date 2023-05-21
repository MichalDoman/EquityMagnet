from django.contrib import admin
from django.urls import path, include
from main_app.views import HomeView, CompanyListView, CompanyDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", HomeView.as_view(), name="home"),
    path("companies/", CompanyListView.as_view(), name="companies"),
    path("company-details/<int:pk>", CompanyDetailView.as_view(), name="company_details"),
]
