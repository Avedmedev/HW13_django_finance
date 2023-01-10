from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CashOutCategories(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class CashInCategories(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class UserCashOutCategories(models.Model):
    cash_out_category = models.ForeignKey(CashOutCategories, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.cash_out_category.name


class UserCashInCategories(models.Model):
    cash_in_category = models.ForeignKey(CashInCategories, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.cash_in_category.name


class Contractor(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class ContractorUser(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CashIn(models.Model):
    cashin = models.FloatField()
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, null=False)
    cashin_category = models.ForeignKey(UserCashInCategories, on_delete=models.PROTECT, null=False)
    description = models.CharField(max_length=150, null=True, blank=True)
    transacted = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self.cashin)} from {self.contractor.name} on {self.date}"


class CashOut(models.Model):
    cashout = models.FloatField()
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT, null=False)
    cashout_category = models.ForeignKey(UserCashOutCategories, on_delete=models.PROTECT, null=False)
    description = models.CharField(max_length=150, null=True, blank=True)
    transacted = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cashout} hrn to {self.contractor.name} on {self.date}"


class Balance(models.Model):
    cash = models.FloatField()
    last_modified = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Balance {self.user}'s account: {self.cash} hrn"
