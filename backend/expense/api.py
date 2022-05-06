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
