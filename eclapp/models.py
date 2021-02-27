from django.db import models

# Create your models here.

'''
AccountHeads{
	id <primary_key>
	name <character_field>
}
'''


class AccountHeads(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.name}'


'''
AccountType{
	id <primary_key>
	acc_type_name <character_field>
	acc_head <foreign_key AccountHeads>
}
'''


class AccountType(models.Model):
    acc_type_name = models.CharField(max_length=60)
    acc_head = models.ForeignKey(
        AccountHeads, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.acc_type_name} , {self.acc_head}'


'''
AccountName{
	id <primary_key>
	acc_name <character_field>
	type_of_acc <foreign_key AccountType>
	opening_balance <float_field>
	closing_balance <float_field>
}
'''


class AccountName(models.Model):
    acc_name = models.CharField(max_length=60)
    type_of_acc = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    opening_balance = models.FloatField()
    closing_balance = models.FloatField()

    def __str__(self):
        return f'{self.acc_name} , {self.type_of_acc}'


'''
JournalLog{
	id <primary_key>
	transaction_date <datetime_field>
	reference_no <character_field>
}
'''


class JournalLog(models.Model):
    transaction_date = models.DateField()
    reference_no = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.transaction_date} , {self.reference_no}'


'''
JournalLogDetails{
	id <primary_key>
	journal_log <foreign_key JournalLog>
	account_name <foreign_key AccountName>
	amount <float_field> 
}
'''


class JournalLogDetails(models.Model):
    journal_log = models.ForeignKey(JournalLog, on_delete=models.CASCADE)
    account_name = models.ForeignKey(AccountName, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f'{self.account_name} , {self.amount}'
