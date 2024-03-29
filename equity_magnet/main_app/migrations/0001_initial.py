# Generated by Django 4.2.1 on 2023-05-16 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('market_cap', models.IntegerField()),
                ('website', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('exchanges', models.ManyToManyField(to='main_app.exchange')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_value', models.FloatField()),
                ('history', models.JSONField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company')),
            ],
        ),
        migrations.CreateModel(
            name='IncomeStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('total_revenue', models.IntegerField()),
                ('cost_of_revenue', models.IntegerField()),
                ('gross_profit', models.IntegerField()),
                ('gross_profit_ratio', models.IntegerField()),
                ('research_and_development_expenses', models.IntegerField()),
                ('general_and_administrative_expenses', models.IntegerField()),
                ('selling_and_marketing_expenses', models.IntegerField()),
                ('selling_general_and_administrative_expenses', models.IntegerField()),
                ('other_expenses', models.IntegerField()),
                ('operating_expenses', models.IntegerField()),
                ('cost_and_expenses', models.IntegerField()),
                ('interest_income', models.IntegerField()),
                ('interest_expense', models.IntegerField()),
                ('depreciation_and_amortization', models.IntegerField()),
                ('ebitda', models.IntegerField()),
                ('ebitda_ratio', models.FloatField()),
                ('operating_income', models.IntegerField()),
                ('operating_income_ratio', models.FloatField()),
                ('total_other_income_expenses_net', models.IntegerField()),
                ('income_before_tax', models.IntegerField()),
                ('income_before_tax_ratio', models.FloatField()),
                ('income_tax_expense', models.IntegerField()),
                ('net_income', models.IntegerField()),
                ('net_income_ratio', models.FloatField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='exchange',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.exchange'),
        ),
        migrations.AddField(
            model_name='company',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.sector'),
        ),
        migrations.CreateModel(
            name='CashFlowStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('net_income', models.IntegerField()),
                ('depreciation_and_amortization', models.IntegerField()),
                ('deferred_income_tax', models.IntegerField()),
                ('stock_based_compensation', models.IntegerField()),
                ('change_in_working_capital', models.IntegerField()),
                ('accounts_receivables', models.IntegerField()),
                ('inventory', models.IntegerField()),
                ('account_payables', models.IntegerField()),
                ('other_working_capitals', models.IntegerField()),
                ('other_non_cash_items', models.IntegerField()),
                ('net_cash_provided_by_operating_activities', models.IntegerField()),
                ('investments_in_property_plant_and_equipment', models.IntegerField()),
                ('acquisitions_net', models.IntegerField()),
                ('purchases_of_investments', models.IntegerField()),
                ('sales_maturities_of_investments', models.IntegerField()),
                ('other_investing_activities', models.IntegerField()),
                ('net_cash_used_for_investing_activities', models.IntegerField()),
                ('debt_repayment', models.IntegerField()),
                ('common_stock_issued', models.IntegerField()),
                ('common_stock_repurchased', models.IntegerField()),
                ('dividends_paid', models.IntegerField()),
                ('other_financing_activities', models.IntegerField()),
                ('net_cash_used_provided_by_financing_activities', models.IntegerField()),
                ('effect_of_forex_changes_on_cash', models.IntegerField()),
                ('net_change_in_cash', models.IntegerField()),
                ('cash_at_end_of_period', models.IntegerField()),
                ('cash_at_beginning_of_period', models.IntegerField()),
                ('operating_cash_flow', models.IntegerField()),
                ('capital_expenditure', models.IntegerField()),
                ('free_cash_flow', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company')),
            ],
        ),
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('cash_and_cash_equivalents', models.IntegerField()),
                ('short_term_investments', models.IntegerField()),
                ('cash_and_short_term_investments', models.IntegerField()),
                ('net_receivables', models.IntegerField()),
                ('inventory', models.IntegerField()),
                ('other_current_assets', models.IntegerField()),
                ('total_current_assets', models.IntegerField()),
                ('property_plant_equipment_net', models.IntegerField()),
                ('goodwill', models.IntegerField()),
                ('intangible_assets', models.IntegerField()),
                ('goodwill_and_intangible_assets', models.IntegerField()),
                ('long_term_investments', models.IntegerField()),
                ('tax_assets', models.IntegerField()),
                ('other_non_current_assets', models.IntegerField()),
                ('total_non_current_assets', models.IntegerField()),
                ('other_assets', models.IntegerField()),
                ('total_assets', models.IntegerField()),
                ('account_payables', models.IntegerField()),
                ('short_term_debt', models.IntegerField()),
                ('tax_payables', models.IntegerField()),
                ('deferred_revenue', models.IntegerField()),
                ('other_current_liabilities', models.IntegerField()),
                ('total_current_liabilities', models.IntegerField()),
                ('long_term_debt', models.IntegerField()),
                ('deferred_revenue_non_current', models.IntegerField()),
                ('deferred_tax_liabilities_non_current', models.IntegerField()),
                ('other_non_current_liabilities', models.IntegerField()),
                ('total_non_current_liabilities', models.IntegerField()),
                ('other_liabilities', models.IntegerField()),
                ('capital_lease_obligations', models.IntegerField()),
                ('total_liabilities', models.IntegerField()),
                ('preferred_stock', models.IntegerField()),
                ('common_stock', models.IntegerField()),
                ('retained_earnings', models.IntegerField()),
                ('accumulated_other_comprehensive_income_loss', models.IntegerField()),
                ('other_total_stockholder_equity', models.IntegerField()),
                ('total_stock_holder_equity', models.IntegerField()),
                ('total_equity', models.IntegerField()),
                ('total_liabilities_and_stock_holder_equity', models.IntegerField()),
                ('minority_interest', models.IntegerField()),
                ('total_liabilities_and_total_equity', models.IntegerField()),
                ('total_investments', models.IntegerField()),
                ('total_debt', models.IntegerField()),
                ('net_debt', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.company')),
            ],
        ),
    ]
