from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.orm import create_schema

from .models import Customer, Expense

router = Router()

CustomerSchema = create_schema(Customer)
ExpenseSchema = create_schema(Expense)


class CustomerSchemaIn(Schema):
    name: str


class ExpenseSchemaIn(Schema):
    due_date: str
    description: str
    customer_id: int
    value: float


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


@router.get("/expenses", response=List[ExpenseSchema])
def list_expenses(request):
    qs = Expense.objects.all()
    return qs


@router.get("/expenses/{id}", response=ExpenseSchema)
def get_expense(request, id: int):
    expense = get_object_or_404(Expense, id=id)
    return expense


@router.post("/expenses", response={201: ExpenseSchema})
def create_expense(request, payload: ExpenseSchemaIn):
    # Get params
    due_date = payload.due_date
    description = payload.description
    customer_id = payload.customer_id
    value = payload.value

    # Instance models
    customer = get_object_or_404(Customer, id=customer_id)

    # Mount dict data
    data = dict(
        due_date=due_date,
        description=description,
        customer=customer,
        value=value,
    )

    # Save data
    expense = Expense.objects.create(**data)

    return 201, expense


@router.put("/expenses/{id}", response=ExpenseSchema)
def update_expense(request, id: int, payload: ExpenseSchemaIn):
    expense = get_object_or_404(Expense, id=id)

    for attr, value in payload.dict().items():
        setattr(expense, attr, value)

    expense.save()
    return expense


@router.delete("/expenses/{id}", response={204: None})
def delete_expense(request, id: int):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return 204, None
