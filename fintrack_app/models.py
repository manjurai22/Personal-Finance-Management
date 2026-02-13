from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def total_balance(self):
        return self.balance
    def __str__(self):
        return self.full_name

class Category(TimeStampModel):
    CATEGORY_TYPE = (
        ("income", "Income"),
        ("expense", "Expense"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPE)
   
    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

class Transaction(TimeStampModel):
    TRANSACTION_TYPE = (
        ("income", "Income"),
        ("expense", "Expense"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.amount} ({self.get_transaction_type_display()})"

class Budget(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    month = models.DateField()

    class Meta:
        ordering = ["-month"]
    
    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')}"
 
class Debt(TimeStampModel):
    DEBT_TYPE = (
        ("lent", "Lent"),
        ("borrowed", "Borrowed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    debt_type = models.CharField(max_length=10, choices=DEBT_TYPE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.0)])
    start_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.title} : {self.remaining_amount}"

class Goal(TimeStampModel):
    GOAL_TYPE = (
        ("savings", "Savings"),
        ("debt_clear", "Debt Clearance"),
        ("purchase", "Purchase"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.0)], default=0)
    deadline = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.current_amount > self.target_amount:
            raise ValidationError({
                "Current amount cannot exceed target amount."
            })

    def __str__(self):
        return f"{self.title} ({self.current_amount}/{self.target_amount})"
    