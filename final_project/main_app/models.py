from django.db import models


class Exchange(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)


class Sector(models.Model):
    name = models.CharField(max_length=255)
    exchange = models.ManyToManyField(Exchange)


class Company(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)


class Price(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    current_value = models.FloatField()
    history = models.JSONField()


class IncomeStatement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.IntegerField()
    income_statement_json = models.JSONField()


class BalanceSheet(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.IntegerField()


class CashFlowStatement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.IntegerField()
