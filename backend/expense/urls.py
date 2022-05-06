from django.urls import include, path
from rest_framework import routers

from backend.expense.api_drf.viewsets import CustomerViewSet, ExpenseViewSet

app_name = 'expense'

router = routers.DefaultRouter()

router.register(r'customers', CustomerViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
