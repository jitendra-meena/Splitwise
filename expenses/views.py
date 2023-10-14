from decimal import Decimal
from django.db import transaction
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import User, Expense, ExpenseParticipant, Balance
from .serializers import UserSerializer, ExpenseSerializer, ExpenseParticipantSerializer, BalanceSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        expense = serializer.instance

        response = split_expense_and_update_balances(expense)

        return Response(response, status=status.HTTP_201_CREATED)

class ExpenseParticipantViewSet(viewsets.ModelViewSet):
    queryset = ExpenseParticipant.objects.all()
    serializer_class = ExpenseParticipantSerializer

class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

def split_expense_and_update_balances(expense):
    participants = ExpenseParticipant.objects.filter(expense=expense)
    total_amount = expense.amount
    
    if expense.expense_type == 'EQUAL':
        share_per_participant = total_amount / len(participants)
    elif expense.expense_type == 'EXACT':
        total_shares = sum(participant.share for participant in participants)
        if total_shares != total_amount:
            return JsonResponse({'error': 'Total shares do not match the total amount.'})
    elif expense.expense_type == 'PERCENT':
        total_percent_share = sum(participant.share for participant in participants)
        if total_percent_share != 100:
            return JsonResponse({'error': 'Total percentage shares do not add up to 100.'})
        share_per_participant = (total_amount * Decimal('0.01')) * participants[0].share

    with transaction.atomic():
        for participant in participants:
            balance = Balance.objects.get_or_create(user_owed_to=participant.participant, user_owed_by=expense.created_by)[0]
            balance.amount += share_per_participant
            balance.save()

    return JsonResponse({'message': 'Expense split and balances updated successfully.'})

def simplify_balances(user):
    balances = Balance.objects.filter(user_owed_to=user)

    for balance in balances:
        negative_balance = Balance.objects.filter(
            user_owed_to=balance.user_owed_by, user_owed_by=user
        ).first()

        if negative_balance:
            if negative_balance.amount >= balance.amount:
                negative_balance.amount -= balance.amount
                balance.amount = 0
            else:
                balance.amount -= negative_balance.amount
                negative_balance.amount = 0

    Balance.objects.filter(user_owed_to=user, amount=0).delete()

