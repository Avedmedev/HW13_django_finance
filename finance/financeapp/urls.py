from django.urls import path

from . import views
from .views import CashOutLog, CashInLog

app_name = "financeapp"

urlpatterns = [
    path('', views.main, name='main'),
    path('cashin/', views.cash_in, name="cashin"),
    path('cashout/', views.cash_out, name="cashout"),
    path('cashinlog/', CashInLog.as_view(), name="cashinlog"),
    path('cashoutlog/', CashOutLog.as_view(), name="cashoutlog"),
    path('cashflowreport/', views.cash_flow_report, name="cashflowreport"),
    path('contractoredit/', views.contractor_edit, name="contractoredit"),
    path('catinedit/', views.cat_in_edit, name="catinedit"),
    path('catoutedit/', views.cat_out_edit, name="catoutedit"),
]
