from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

from main_app.views import HomeView, CompanyListView, CompanyDetailView, ManageFavoritesView, WatchlistView, \
    EvaluationListView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/", LoginView.as_view(extra_context={"success_message": "Logged in successfully!"}),
         name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("", HomeView.as_view(), name="home"),
    path("companies/", CompanyListView.as_view(), name="companies"),
    path("company-details/<int:pk>", CompanyDetailView.as_view(), name="company_details"),
    path("manage-favorites/", ManageFavoritesView.as_view()),
    path("watchlist/", WatchlistView.as_view(), name="watchlist"),
    path("evaluation-list", EvaluationListView.as_view(), name="evaluation_list"),
]
