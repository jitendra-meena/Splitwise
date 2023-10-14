# expenses/serializers.py

from rest_framework import serializers
from .models import User, Expense, ExpenseParticipant, Balance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipant
        fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'
