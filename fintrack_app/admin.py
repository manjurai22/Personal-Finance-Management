from django.contrib import admin
from .models import UserProfile, Category, Debt, Transaction, Budget, Goal, Report
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Debt)
admin.site.register(Goal)
admin.site.register(Report)