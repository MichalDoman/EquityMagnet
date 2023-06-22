# Generated by Django 4.2.1 on 2023-06-02 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='change',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='price',
            name='change_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='price',
            name='shares_outstanding',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='account_payables',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='accumulated_other_comprehensive_income_loss',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='capital_lease_obligations',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='cash_and_cash_equivalents',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='cash_and_short_term_investments',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='common_stock',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='deferred_revenue',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='deferred_revenue_non_current',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='deferred_tax_liabilities_non_current',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='goodwill',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='goodwill_and_intangible_assets',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='intangible_assets',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='inventory',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='long_term_debt',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='long_term_investments',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='minority_interest',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='net_debt',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='net_receivables',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='other_assets',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='other_current_assets',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='other_current_liabilities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='other_liabilities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='other_non_current_assets',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='other_non_current_liabilities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='other_total_stockholder_equity',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='preferred_stock',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='property_plant_equipment_net',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='retained_earnings',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='short_term_debt',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='short_term_investments',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='tax_assets',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='tax_payables',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_assets',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_current_assets',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_current_liabilities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_debt',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_equity',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_investments',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_liabilities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_liabilities_and_stock_holder_equity',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_liabilities_and_total_equity',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_non_current_assets',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_non_current_liabilities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='balancesheet',
            name='total_stock_holder_equity',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='account_payables',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='accounts_receivables',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='acquisitions_net',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='capital_expenditure',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='cash_at_beginning_of_period',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='cash_at_end_of_period',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='change_in_working_capital',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='common_stock_issued',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='common_stock_repurchased',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='debt_repayment',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='deferred_income_tax',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='depreciation_and_amortization',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='dividends_paid',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='effect_of_forex_changes_on_cash',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='free_cash_flow',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='inventory',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='investments_in_property_plant_and_equipment',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='net_cash_provided_by_operating_activities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='net_cash_used_for_investing_activities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='net_cash_used_provided_by_financing_activities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='net_change_in_cash',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='net_income',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='operating_cash_flow',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='other_financing_activities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='other_investing_activities',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='other_non_cash_items',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='other_working_capitals',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='purchases_of_investments',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='sales_maturities_of_investments',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='cashflowstatement',
            name='stock_based_compensation',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='market_cap',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='sector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.sector'),
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='cost_and_expenses',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='cost_of_revenue',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='depreciation_and_amortization',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='ebitda',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='general_and_administrative_expenses',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='gross_profit',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='gross_profit_ratio',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='income_before_tax',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='income_tax_expense',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='interest_expense',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='interest_income',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='net_income',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='operating_expenses',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='operating_income',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='other_expenses',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='research_and_development_expenses',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='selling_and_marketing_expenses',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='selling_general_and_administrative_expenses',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='total_other_income_expenses_net',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='incomestatement',
            name='total_revenue',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='price',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.company'),
        ),
        migrations.CreateModel(
            name='FavoriteCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'company')},
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField(auto_now_add=True)),
                ('expiration_date', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'company')},
            },
        ),
    ]