from django.db.models.query import ValuesListIterable
import graphene
from graphene.types.scalars import Int
from graphene_django import DjangoObjectType
from .models import *
from django.db.models import Q
from django.http import JsonResponse
import datetime


class AccountHeadsType(DjangoObjectType):
    class Meta:
        model = AccountHeads
        fields = "__all__"


class AccountNameType(DjangoObjectType):
    class Meta:
        model = AccountName
        fields = "__all__"


class AccountTypeType(DjangoObjectType):
    class Meta:
        model = AccountType
        fields = "__all__"


class JournalLogType(DjangoObjectType):
    class Meta:
        model = JournalLog
        fields = "__all__"


class JournalLogDetailsType(DjangoObjectType):
    class Meta:
        model = JournalLogDetails
        fields = "__all__"


class Query(graphene.ObjectType):
    all_account_heads = graphene.List(AccountHeadsType)
    all_account_names = graphene.List(AccountNameType)
    all_account_types = graphene.List(AccountTypeType)
    all_journal_logs = graphene.List(JournalLogType)
    all_journal_log_details = graphene.List(JournalLogDetailsType)
    cashflow_calculator = graphene.JSONString(number_of_month=graphene.Int())

    # If AccountHead name of a JournalLogDetails is 'Assets' and AccountType name is "Cash and Bank",
    # the JournalLogDetails amount will be added under < cash > variable month and year wise.
    # SELECT transaction_date, amount
    # FROM journal_log_details
    # INNER JOIN journal_log
    # ON journal_log_details.journal_log_id = journal_log.id
    '''
    -- SELECT transaction_date, amount
-- FROM journal_log_details
-- INNER JOIN journal_log
-- ON journal_log_details.journal_log_id = journal_log.id;
SELECT transaction_date
FROM journal_log
WHERE transaction_date < 2021-02-26 09:22:34;
            acc_id = AccountHeads.objects.values_list(
            'id', flat=True).filter(name__exact="Assets")
        acc_ty_name = AccountType.objects.values_list(
            'id', flat=True).filter(acc_type_name__exact="Cash and Bank")
        cash = JournalLogDetails.objects.values_list(
            'amount', flat=True).filter(account_name_id=acc_id)
        return Int(AccountHeads.objects.values_list(
            'id', flat=True).filter(name__exact="Assets"))
SELECT transaction_date, amount
FROM journal_log_details
INNER JOIN journal_log
ON journal_log_details.journal_log_id = journal_log.id
WHERE transaction_date<="2021-02-21" LIMIT 2;

    '''
# credit : https://github.com/ovibinzia1885/interview_work/blob/09a84e5440bec715dd54fb4fae891c8677666ada/intern%20view/core/views.py

    def resolve_cashflow_calculator(self, info, number_of_month):
        titles = list()
        year = datetime.date.today().year
        month = datetime.date.today().month
        for months in range(number_of_month):
            jlogs = JournalLogDetails.objects.filter(
                journal_log__transaction_date__year=year,
                journal_log__transaction_date__month=month,
            )
            cash = 0
            income = 0
            expense = 0
            for j in jlogs:
                if j.account_name.type_of_acc.acc_head.name == 'Assets' and j.account_name.type_of_acc.acc_type_name == 'Cash and Bank':
                    cash = cash + j.amount
                elif j.account_name.type_of_acc.acc_head.name == 'Income':
                    income = income + j.amount
                elif j.account_name.type_of_acc.acc_head.name == 'Expense':
                    expense = expense + j.amount

            cashflow = (cash + income) - expense

            p = {
                'year':   year,
                'month':  month,
                'amount': cashflow,

            }
            titles.append(p)
            print(month)
            print(year)
            if month - 1 < 1:
                month = 12
                year = year - 1
            else:
                month = month - 1

        return titles

    def resolve_all_account_heads(self, info, **args):
        return AccountHeads.objects.all()

    def resolve_all_account_names(self, info, **args):
        return AccountName.objects.all()

    def resolve_all_account_types(self, info, **args):
        return AccountType.objects.all()

    def resolve_all_journal_logs(self, info, **args):
        return JournalLog.objects.all()

    def resolve_all_journal_log_details(self, info, **args):
        return JournalLogDetails.objects.all()


schema = graphene.Schema(query=Query)
