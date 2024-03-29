import json
from random import sample

from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.models import Company, Price, FavoriteCompany, Evaluation, IncomeStatement, BalanceSheet, \
    CashFlowStatement
from main_app.utils.general_utils import extract_historical_prices, get_all_countries, get_field_dictionaries, \
    SORTING_NAMES
from main_app.utils.evaluation_utils import DiscountedCashFlow
from main_app.forms import SearchFiltersForm, EvaluationEditablesForm, RegisterForm


class HomeView(View):
    """A view supporting GET method, that represents the Home Page of the app.

    :return: an HTTPResponse that passes a context to the home.html template.
    The context contain a random sample of companies from database and their price models.
    """

    def get(self, request):
        all_companies = Company.objects.select_related("exchange", "sector")
        sample_companies = sample(list(all_companies), 4)
        prices = [Price.objects.get(company=c) for c in sample_companies]

        return render(request, "home.html", context={
            "companies": zip(sample_companies, prices)
        })


class CompanyListView(ListView):
    """A generic list view for displaying paginated list of companies.
    The view uses a form for filtering the list."""
    model = Company
    paginate_by = 10
    form_class = SearchFiltersForm

    def get_queryset(self):
        """Queryset is set based on the filters requested by the user.
        Regardless filters queryset can be sorted."""

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
        if sort_by in SORTING_NAMES:
            queryset = queryset.order_by(sort_by)
        return queryset

    def get_context_data(self, **kwargs):
        """
        Add form and url part to the context.
        This url part allows to sort and paginate filtered data.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        if self.request.user.is_authenticated:
            favorites_obj = FavoriteCompany.objects.filter(user=self.request.user)
            context['favorites'] = [favorite.company for favorite in favorites_obj]

        # Get sorting and paginating main url part:
        if self.request.method == 'GET':
            phrase = self.request.GET.get('phrase', '')
            exchanges = self.request.GET.getlist('exchanges', [])
            sectors = self.request.GET.getlist('sectors', [])
            countries = self.request.GET.getlist('countries', [])
            market_cap = self.request.GET.get('market_cap', '')

            url = f"&phrase={phrase}"
            for i, category in enumerate([exchanges, sectors, countries]):
                for index in category:
                    if i == 0:
                        url += f"&exchanges={index}"
                    elif i == 1:
                        url += f"&sectors={index}"
                    else:
                        url += f"&countries={index}"

            url += f"&market_cap={market_cap}"

            context['url_part'] = url

        return context


class CompanyDetailView(DetailView):
    """A generic detail view of Company object's details."""
    model = Company
    context_object_name = "company"

    def get_context_data(self, **kwargs):
        """Extend context by company's financial statements and all of their field names"""

        context = super().get_context_data(**kwargs)

        # Add company's price data to the context:
        price = Price.objects.get(company=self.kwargs['pk'])
        context['price'] = price

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
    """ A view that enables management of favorites through javascript POST request.
    This view is connected to the favorites.js file."""

    def post(self, request):
        """If user is logged in, add a company to user's favorites or remove it if it is already there."""

        response = {"is_authenticated": request.user.is_authenticated}
        if response['is_authenticated']:
            company_id = request.POST["company_id"][0]
            company = Company.objects.get(pk=company_id)

            is_favorite = FavoriteCompany.objects.filter(user=request.user, company=company).exists()
            if is_favorite:
                FavoriteCompany.objects.get(user=request.user, company=company).delete()
            else:
                FavoriteCompany.objects.create(user=request.user, company=company)

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
    """A view with all calculations and results of dcf evaluation.
    This view uses a form to get certain values, customized by the user."""
    model = Company
    context_object_name = "company"
    template_name_suffix = "_evaluation"
    form_class = EvaluationEditablesForm

    def get_context_data(self, **kwargs):
        """This view gets data from the form and calculates dcf basing on it.
        All dcf data is divided into smaller data structures,
        mostly dictionaries and are displayed in separate tables or divs.
        Therefore, it is also separately added to the context."""

        context = super().get_context_data(**kwargs)
        form = self.form_class(self.request.GET)
        context['form'] = form
        company = Company.objects.get(pk=self.kwargs['pk'])

        wacc = g = revenue_rate = operational_costs = tax = other_operational_costs = None

        if form.is_valid():
            wacc = form.cleaned_data['wacc']
            g = form.cleaned_data['g']
            revenue_rate = form.cleaned_data['revenue_rate']
            operational_costs = form.cleaned_data['operational_costs']
            tax = form.cleaned_data['tax']
            other_operational_costs = form.cleaned_data['other_operational_costs']

        income_statements = IncomeStatement.objects.filter(company=company).order_by("year")
        balance_sheets = BalanceSheet.objects.filter(company=company).order_by("year")
        cash_flow_statements = CashFlowStatement.objects.filter(company=company).order_by("year")
        current_price = Price.objects.get(company=company).current_value

        evaluation = DiscountedCashFlow(income_statements, balance_sheets, cash_flow_statements)

        # Get dcf_index for highlighting projection data:
        context["dcf_index"] = evaluation.dcf_index

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

        # Get dcf contexts:
        context['dcf_data'] = evaluation.get_dcf_dict(
            wacc,
            g
        )
        context["share_value"] = evaluation.get_share_value_dict(current_price, company.market_cap)

        return context


class RegisterView(FormView):
    """A view that enables the user to create an account and access favorites and evaluation functionalities."""
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Check if registration conditions are met. If so create an account and log in the user.
        Otherwise, return invalid form error."""
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
