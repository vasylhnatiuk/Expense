from django.contrib import admin
from .models import User, Expense

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')
    ordering = ('id',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'date', 'category', 'user')
    list_filter = ('category', 'date')
    search_fields = ('title', 'category', 'user__username')
    ordering = ('date',)
    date_hierarchy = 'date'
