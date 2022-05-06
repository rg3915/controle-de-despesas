from rest_framework import viewsets

from backend.expense.api_drf.serializers import (
    CustomerSerializer,
    ExpenseSerializer
)
from backend.expense.models import Customer, Expense


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
