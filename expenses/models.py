from decimal import Decimal
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)

class Expense(models.Model):
    EXPENSE_TYPES = (
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENT', 'Percent'),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(choices=EXPENSE_TYPES, max_length=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=10, decimal_places=2)

class Balance(models.Model):
    user_owed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances_owed')
    user_owed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances_owing')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
