from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ExpenseViewSet, ExpenseParticipantViewSet, BalanceViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'expense-participants', ExpenseParticipantViewSet)
router.register(r'balances', BalanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
