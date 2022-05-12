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
        'paid',
    )
    list_display_links = ('__str__',)
    search_fields = ('description', 'customer__name')
    list_filter = ('paid',)
    date_hierarchy = 'due_date'
