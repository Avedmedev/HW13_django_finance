from datetime import datetime

from django.contrib.auth import decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView

from .forms import CashInForm, CashOutForm, ReportForm, ContractorForm
from .models import CashOut, CashIn
from .utils import get_user_current_balance, set_user_current_balance, get_report_data, get_total_for_report, \
    get_report_data_orm, get_total_for_report_orm


def main(request):
    return render(request, "financeapp/pages/index.html", context={})


@decorators.login_required
def cash_in(request):
    if request.method == "POST":
        form = CashInForm(request.POST)

        if not form.is_valid():
            return render(request, 'financeapp/pages/cashin.html', context={'form': form})

        cashin = form.save(commit=False)

        if cashin.cashin < 0:
            bc = get_user_current_balance(request.user)
            if bc and (bc.cash + cashin.cashin) < 0:
                form.add_error('cashin', 'There is not enough cash on balance')
                return render(request, 'financeapp/pages/cashin.html', context={'form': form})

        cashin.user = request.user
        cashin.save()
        set_user_current_balance(request.user, cashin.cashin)
        return redirect(to='financeapp:main')

    return render(request, 'financeapp/pages/cashin.html', context={'form': CashInForm()})


@decorators.login_required
def cash_out(request):
    if request.method == "POST":
        form = CashOutForm(request.POST)

        if not form.is_valid():
            return render(request, 'financeapp/pages/cashout.html', context={'form': form})

        cashout = form.save(commit=False)

        bc = get_user_current_balance(request.user)
        if bc and (bc.cash - cashout.cashout) < 0:
            form.add_error('cashout', 'There is not enough cash on balance')
            return render(request, 'financeapp/pages/cashout.html', context={'form': form})

        cashout.user = request.user
        cashout.save()
        set_user_current_balance(request.user, -cashout.cashout)
        return redirect(to='financeapp:main')

    return render(request, 'financeapp/pages/cashout.html', context={'form': CashOutForm()})


class CashInLog(LoginRequiredMixin, ListView):
    model = CashIn
    template_name = 'financeapp/pages/cashinlog.html'
    context_object_name = 'cash_in'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return CashIn.objects.filter(transacted=True, user=self.request.user).order_by('-date').all()


class CashOutLog(LoginRequiredMixin, ListView):
    model = CashOut
    template_name = 'financeapp/pages/cashoutlog.html'
    context_object_name = 'cash_out'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return CashOut.objects.filter(transacted=True, user=self.request.user).all()


@decorators.login_required
def cash_flow_report(request):
    if request.method == "POST":

        filterdata = {}

        form = ReportForm(request.POST)

        if not form.is_valid():
            return render(request, 'financeapp/pages/cashflowreport.html', context={'form': form})

        d = form.data
        filterdata['in_out'] = d.get('in_out')
        filterdata['start'] = datetime(*list(map(lambda x: int(d.get(f'start_{x}')), ['year', 'month', 'day'])))
        filterdata['end'] = datetime(*list(map(lambda x: int(d.get(f'end_{x}')), ['year', 'month', 'day'])))

        # reportdata = get_report_data(request.user, filterdata)
        # total = get_total_for_report(reportdata)

        reportdata = get_report_data_orm(request.user, filterdata)
        total = get_total_for_report_orm(reportdata)

        return render(request, 'financeapp/pages/cashflowreport.html',
                      context={'form': form, 'reportdata': reportdata, 'total': total})

    return render(request, 'financeapp/pages/cashflowreport.html', context={'form': ReportForm()})


@decorators.login_required
def contractor_edit(request):

    if request.method == "POST":
        form = ContractorForm(request.POST)

        if not form.is_valid():
            return render(request, 'financeapp/edit/contractoredit.html', context={'form': form})

    return render(request, 'financeapp/edit/contractoredit.html', context={'form': ContractorForm()})


@decorators.login_required
def cat_in_edit(request):
    return render(request, 'financeapp/edit/catinedit.html', context={})


@decorators.login_required
def cat_out_edit(request):
    return render(request, 'financeapp/edit/catoutedit.html', context={})
