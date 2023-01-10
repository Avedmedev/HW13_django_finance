from datetime import timedelta
from typing import List

from django.contrib.auth.models import User
from django.db import connection, models
from django.db.models import QuerySet, F

from .models import Balance, CashIn, CashOut


def get_user_current_balance(user):
    bc = Balance.objects.filter(user=user).first()

    return bc if bc else None


def set_user_current_balance(user, cashin):
    bc = get_user_current_balance(user)

    if bc is None:
        bc = Balance(cash=0.0, user=user)

    bc.cash += cashin
    bc.save()


def get_total_for_report_orm(data: QuerySet) -> float:
    total = float()
    for row in data:
        total = total + row['cashflow'] if row['type'] == 1 else total - row['cashflow']
    return total


def get_cashin_data(user, filterdata: dict) -> QuerySet:

    q = CashIn.objects.filter(
        user=user,
        transacted=True,
        date__gte=filterdata['start'],
        date__lte=filterdata['end']
    ).all().values(
        'description',
        'date',
    ).annotate(
        cashflow=F('cashin'),
        category=F('cashin_category__cash_in_category__name'),
        contractor=F('contractor__name'),
        type=F('cashin')*0 + 1
    )

    return q


def get_cashout_data(user, filterdata: dict) -> QuerySet:

    q = CashOut.objects.filter(
        user=user,
        transacted=True,
        date__gte=filterdata['start'],
        date__lte=filterdata['end']
    ).all().values(
        'description',
        'date',
    ).annotate(
        cashflow=F('cashout'),
        category=F('cashout_category__cash_out_category__name'),
        contractor=F('contractor__name'),
        type=F('cashout')*0
    )

    return q


def get_report_data_orm(user, filterdata: dict) -> QuerySet:
    match filterdata['in_out']:
        case 'opt1':
            q1 = get_cashin_data(user, filterdata)
            q2 = get_cashout_data(user, filterdata)
            q = q1.union(q2).order_by('-date')
            return q
        case 'opt2':
            q = get_cashin_data(user, filterdata).order_by('-date')
            return q
        case 'opt3':
            q = get_cashout_data(user, filterdata).order_by('-date')
            return q


""" non useful functions """
def get_total_for_report(data: List[tuple]) -> float:
    total = float()
    for row in data:
        total = total + row[0] if row[-1] == 'cashin' else total - row[0]
    return total


def get_report_data(user, filterdata: dict) -> List[tuple]:
    with open("financeapp/sql/query.sql", "r", encoding='utf-8') as fd:
        script = fd.read()

    user_id = User.objects.get(username=user).pk

    in_out_filter = {
        'opt1': [user_id, filterdata['start'], filterdata['end'],
                 user_id, filterdata['start'], filterdata['end']],  # in_out
        'opt2': [user_id, filterdata['start'], filterdata['end'],
                 user_id, filterdata['end'] + timedelta(1), filterdata['end']],  # in
        'opt3': [user_id, filterdata['end'] + timedelta(1), filterdata['end'],
                 user_id, filterdata['start'], filterdata['end']]  # out
    }

    with connection.cursor() as cursor:
        cursor.execute(script, in_out_filter[filterdata['in_out']])
        q = cursor.fetchall()

    return q
