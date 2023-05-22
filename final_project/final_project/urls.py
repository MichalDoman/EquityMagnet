from django.contrib import admin
from django.urls import path, include
from main_app.views import HomeView, CompanyListView, CompanyDetailView, Favorites, Evaluations

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", HomeView.as_view(), name="home"),
    path("companies/", CompanyListView.as_view(), name="companies"),
    path("company-details/<int:pk>", CompanyDetailView.as_view(), name="company_details"),
    path("favorites/<int:pk>", Favorites.as_view(), name="favorites"),
    path("evaluations/<int:pk>", Evaluations.as_view(), name="evaluations"),
]
