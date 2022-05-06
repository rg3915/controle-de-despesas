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
