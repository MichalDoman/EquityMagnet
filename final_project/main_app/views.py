import json
from random import sample

from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.models import Company, Price, FavoriteCompany, Evaluation, IncomeStatement, BalanceSheet, \
    CashFlowStatement
from main_app.utils.general_utils import extract_historical_prices, get_all_countries, get_field_dictionaries
from main_app.utils.evaluation_utils import DiscountedCashFlow
from main_app.forms import SearchFiltersForm, EvaluationEditablesForm, RegisterForm


class HomeView(View):
    """A view supporting GET method, that represents the Home Page of the app.

    :return: an HTTPResponse that passes a context to the home.html template.
    The context contain a random sample of companies from database.
    """

    def get(self, request):
        all_companies = Company.objects.select_related("exchange", "sector")
        sample_companies = sample(list(all_companies), 4)

        return render(request, "home.html", context={
            "companies": sample_companies
        })


class CompanyListView(ListView):
    model = Company
    paginate_by = 10
    form_class = SearchFiltersForm

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            phrase = form.cleaned_data['phrase']
            exchanges = [exchange for exchange in form.cleaned_data['exchanges']]
            sectors = [sector for sector in form.cleaned_data['sectors']]

            country_list = get_all_countries()
            country_ids = [country for country in form.cleaned_data['countries']]

            market_cap = form.cleaned_data['market_cap']

            if phrase:
                queryset = queryset.filter(name__icontains=phrase) | queryset.filter(symbol__icontains=phrase)

            if exchanges:
                temp_queryset = queryset.filter(exchange=exchanges[0])
                for exchange in exchanges[1:]:
                    temp_queryset = temp_queryset | queryset.filter(exchange=exchange)
                queryset = temp_queryset

            if sectors:
                temp_queryset = queryset.filter(sector=sectors[0])
                for sector in sectors[1:]:
                    temp_queryset = temp_queryset | queryset.filter(sector=sector)
                queryset = temp_queryset

            if country_ids:
                temp_queryset = queryset.filter(country__icontains=country_list[int(country_ids[0])])
                for country_id in country_ids[1:]:
                    temp_queryset = temp_queryset | queryset.filter(country__icontains=country_list[int(country_id)])
                queryset = temp_queryset

            if market_cap:
                queryset = queryset.filter(market_cap__gt=market_cap * 1_000_000)

        sort_by = self.request.GET.get('sort_by', 'pk')
        if sort_by in ['name', '-name', 'symbol', '-symbol', 'exchange', '-exchange', 'country', '-country', 'sector',
                       '-sector', 'market_cap', '-market_cap']:
            queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context


class CompanyDetailView(DetailView):
    model = Company
    context_object_name = "company"

    def get_context_data(self, **kwargs):
        """Extend context by company's financial statements and all of their field names"""

        context = super().get_context_data(**kwargs)

        income_statements = IncomeStatement.objects.filter(company=self.kwargs['pk']).order_by("year")
        balance_sheets = BalanceSheet.objects.filter(company=self.kwargs['pk']).order_by("year")
        cash_flow_statements = CashFlowStatement.objects.filter(company=self.kwargs['pk']).order_by("year")

        # Add company's financial statements to the context:
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
                messages.info(request, f"{company.symbol} was removed from favorites.")
            else:
                FavoriteCompany.objects.create(user=request.user, company=company)
                messages.add_message(request, messages.SUCCESS, f"{company.symbol} was added to favorites.")

            response["is_favorite"] = is_favorite
            return JsonResponse(response)

        return JsonResponse(response)


class BaseListView(ListView):
    """Base ListView for list of favorites and evaluations"""

    def get_context_data(self, **kwargs):
        """Extract a list o Company objects from FavoriteCompany and
        Evaluation models for currently logged user and adds it to the context"""

        context = super().get_context_data(**kwargs)
        companies = []
        if self.request.user.is_authenticated:
            user = self.request.user

            user_assigned_objects = self.model.objects.filter(user=user)
            for user_assigned_object in user_assigned_objects:
                companies.append(user_assigned_object.company)

        context["companies"] = companies
        return context


class WatchlistView(BaseListView):
    model = FavoriteCompany


class EvaluationListView(BaseListView):
    model = Evaluation


class EvaluationView(DetailView):
    model = Company
    context_object_name = "company"
    template_name_suffix = "_evaluation"
    form_class = EvaluationEditablesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.form_class(self.request.GET)
        context['form'] = form

        wacc = g = revenue_rate = operational_costs = tax = other_operational_costs = None

        if form.is_valid():
            wacc = form.cleaned_data['wacc']
            g = form.cleaned_data['g']
            revenue_rate = form.cleaned_data['revenue_rate']
            operational_costs = form.cleaned_data['operational_costs']
            tax = form.cleaned_data['tax']
            other_operational_costs = form.cleaned_data['other_operational_costs']

        income_statements = IncomeStatement.objects.filter(company=self.kwargs['pk']).order_by("year")
        balance_sheets = BalanceSheet.objects.filter(company=self.kwargs['pk']).order_by("year")
        cash_flow_statements = CashFlowStatement.objects.filter(company=self.kwargs['pk']).order_by("year")

        evaluation = DiscountedCashFlow(income_statements, balance_sheets, cash_flow_statements)

        # Get projection context:
        context['income_projection'] = evaluation.get_income_projection_dict(
            revenue_rate,
            operational_costs,
            other_operational_costs,
            tax
        )
        context['turnover_ratios'] = evaluation.get_turnover_ratios_dict()
        context['average_turnover_ratios'] = evaluation.average_turnover_ratios
        context['net_working_capital'] = evaluation.get_net_working_capital_dict()
        context['capex_and_amortization'] = evaluation.get_capex_dict()

        # Get dcf context:
        context['dcf_data'] = evaluation.get_dcf_dict(
            wacc,
            g
        )

        return context


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password_repeated = form.cleaned_data['password_repeated']

        if User.objects.filter(email=email).exists():
            form.add_error(None, 'This e-mail address is already taken!')
            return super().form_invalid(form)

        if password != password_repeated:
            form.add_error(None, 'Passwords did not match!')
            return super().form_invalid(form)

        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        login(self.request, user)
        return super().form_valid(form)
