from django.contrib import admin
from . models import AccountHeads, AccountType, AccountName, JournalLog, JournalLogDetails
# Register your models here.
admin.site.register(AccountHeads)
admin.site.register(AccountType)
admin.site.register(AccountName)
admin.site.register(JournalLog)
admin.site.register(JournalLogDetails)
