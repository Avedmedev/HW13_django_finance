from django.contrib import admin

# Register your models here.
from . import models


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'cash', 'last_modified')


admin.site.register(models.Balance, BalanceAdmin)
admin.site.register(models.CashOutCategories)
admin.site.register(models.CashInCategories)
admin.site.register(models.CashOut)
admin.site.register(models.CashIn)
admin.site.register(models.Contractor)
admin.site.register(models.ContractorUser)
admin.site.register(models.UserCashOutCategories)
admin.site.register(models.UserCashInCategories)
