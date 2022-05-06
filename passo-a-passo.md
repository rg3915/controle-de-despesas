# Passo a passo

* Crie a virtualenv

```
python -m venv .venv
```


* Ative a virtualenv

```
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux
```

* Instale as bibliotecas

```
pip install django-ninja dr_scaffold djangorestframework django-extensions python-decouple
```

* Crie `requirements.txt`

```
Django==4.0.4
django-extensions==3.1.5
django-ninja==0.17.0
djangorestframework==3.13.1
dr-scaffold==2.1.2
python-decouple==3.6
```

* Gere o `.env`

```
python contrib/env_gen.py

cat .env
```

## Criando o projeto

* Crie o projeto

```
django-admin startproject backend .
```

* Crie a app core

```
cd backend
python ../manage.py startapp core
cd ..
```

* Configure `settings.py`

```python
# settings.py

from decouple import config

SECRET_KEY = config('SECRET_KEY')


INSTALLED_APPS = [
    ...
    # apps de terceiros
    'rest_framework',
    'django_extensions',
    'dr_scaffold',
    # minhas apps
    'backend.core',
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

```

* Edite `core/apps.py`

```python
...
name = 'backend.core'
```

* Rode o comando de migração para criar o banco de dados.

```
python manage.py migrate
```

* Crie um super usuário.

```
python manage.py createsuperuser --username="admin" --email=""
```

## Usando dr_scaffold

* Rode o comando a seguir para criar uma app.

```
python manage.py \
dr_scaffold expense Expense \
due_date:datefield \
description:textfield \
customer:foreignkey:Customer \
value:decimalfield \
paid:booleanfield
```

* Copie a pasta para dentro de `backend`.

```
mv expense backend
```

* Edite `settings.py`

```python
# settings.py

INSTALLED_APPS = [
    ...
    # minhas apps
    'backend.core',
    'backend.expense',
]
```

* Edite `expense/apps.py`.

```python
# expense/apps.py
...
name = 'backend.expense'
```


* Edite `expense/models.py`.

```python
# expense/models.py
from django.db import models


class Customer(models.Model):
    name = models.CharField('Nome', max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Expense(models.Model):
    due_date = models.DateField('Data de vencimento')
    description = models.TextField('Descrição', null=True, blank=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name='Pago a',
        related_name='expenses',
        null=True
    )
    value = models.DecimalField(
        'Valor',
        max_digits=5,
        decimal_places=2,
        null=True,
        default=0.0
    )
    paid = models.BooleanField('Pago', default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description}"

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"

```

* Edite `expense/admin.py`

```python
# expense/admin.py
from django.contrib import admin

from backend.expense.models import Customer, Expense


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('name',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'due_date',
        '__str__',
        'customer',
        'value',
        'paid'
    )
    list_display_links = ('__str__',)
    search_fields = ('description', 'customer__name',)
    list_filter = ('paid',)
    date_hierarchy = 'due_date'

```

### Migrações

Rode

```
python manage.py makemigrations
python manage.py migrate
```

### Django REST framework api

Mova `serializers.py` e `views.py` para dentro de uma subpasta chamada `api`.

```
mkdir backend/expense/api
mv backend/expense/serializers.py backend/expense/api/
mv backend/expense/views.py backend/expense/api/viewsets.py
```

* Edite `serializers.py`

```python
# expense/api/serializers.py
from rest_framework import viewsets

from backend.expense.api_drf.serializers import (
    CustomerSerializer,
    ExpenseSerializer
)
from backend.expense.models import Customer, Expense

```

* Edite `viewsets.py`

```python
# expense/api/viewsets.py
from rest_framework import viewsets

from backend.expense.models import Customer, Expense
from backend.expense.serializers import CustomerSerializer, ExpenseSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

```

* Edite `expense/urls.py`

```python
# expense/urls.py
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
```

* Edite `urls.py`

```python
# urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('backend.expense.urls', namespace='expense')),
    path('admin/', admin.site.urls),
]

```

## Django Ninja

Doc: [https://django-ninja.rest-framework.com/](https://django-ninja.rest-framework.com/)

* Edite urls.py

```python
# urls.py
from .api import api

    ...
    path('api/v2/', api.urls),
```

* Crie `backend/api.py`

```python
# api.py
from ninja import NinjaAPI

from backend.expense.api import router as expense_router

api = NinjaAPI()

api.add_router("/expense/", expense_router)

```

* Crie `backend/expense/api.py`

```python
# expense/api.py
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.orm import create_schema

from .models import Customer

router = Router()

CustomerSchema = create_schema(Customer)


class CustomerSchemaIn(Schema):
    name: str


@router.get('/customers', response=List[CustomerSchema])
def list_customers(request):
    qs = Customer.objects.all()
    return qs


@router.get('/customers/{id}', response=CustomerSchema)
def get_Customer(request, id: int):
    customer = get_object_or_404(Customer, id=id)
    return customer


@router.post('/customers', response={201: CustomerSchema})
def create_customer(request, payload: CustomerSchemaIn):
    customer = Customer.objects.create(**payload.dict())
    return 201, customer


@router.put('/customers/{id}', response=CustomerSchema)
def update_customer(request, id: int, payload: CustomerSchemaIn):
    customer = get_object_or_404(Customer, id=id)

    for attr, value in payload.dict().items():
        setattr(Customer, attr, value)

    customer.save()
    return customer


@router.delete('/customers/{id}', response={204: None})
def delete_Customer(request, id: int):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return 204, None

```

## Swagger

http://localhost:8000/api/v2/docs

