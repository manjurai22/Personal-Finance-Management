from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Category, Transaction, Budget, Debt, Goal
from datetime import datetime, timedelta, date
import json
# Create your views here.
@login_required
def dashboard(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={"full_name": user.username}
        )
    
    today = date.today()
    # All user transactions
    transactions = Transaction.objects.filter(user=user)

    # ===== Income & Expense =====
    income = transactions.filter(
        transaction_type="income"
    ).aggregate(total=Sum("amount"))["total"] or 0

    expense = transactions.filter(
        transaction_type="expense"
    ).aggregate(total=Sum("amount"))["total"] or 0

    saved = income - expense

    # ===== Today's Transaction Count =====
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(days=1)

    today_count = transactions.filter(date__gte=start, date__lt=end).count()

    # ===== Monthly Expense =====
    month_start = datetime(today.year, today.month, 1)
    next_month = (month_start + timedelta(days=32)).replace(day=1)

    monthly_expense = transactions.filter(
        transaction_type="expense",
        date__gte=month_start,
        date__lt=next_month
    ).aggregate(total=Sum("amount"))["total"] or 0


    # ===== Monthly Budget =====
    budget = Budget.objects.filter(
        user=user,
        month__year=today.year,
        month__month=today.month
    ).aggregate(total=Sum("monthly_limit"))["total"] or 0

    budget_left = budget - monthly_expense

    # ===== Category Expenses =====
    category_expenses = transactions.filter(
        transaction_type="expense"
    ).values("category__name").annotate(
        total=Sum("amount")
    )
    category_labels = json.dumps(
        [c["category__name"] for c in category_expenses]
    )

    category_totals = json.dumps(
       [float(c["total"]) for c in category_expenses]
     )
    
    # ===== Income & Expense by Category (for grouped bar chart) =====
    income_categories = transactions.filter(transaction_type="income") \
                                    .values("category__name") \
                                    .annotate(total=Sum("amount"))
    expense_categories = transactions.filter(transaction_type="expense") \
                                     .values("category__name") \
                                     .annotate(total=Sum("amount"))

    income_cat_labels = json.dumps([c["category__name"] for c in income_categories])
    income_cat_totals = json.dumps([float(c["total"]) for c in income_categories])
    expense_cat_labels = json.dumps([c["category__name"] for c in expense_categories])
    expense_cat_totals = json.dumps([float(c["total"]) for c in expense_categories])
    


    # ===== Recent Transactions =====
    recent_transactions = transactions.select_related(
        "category"
    ).order_by("-date")[:8]

    # Goals
    goals = Goal.objects.filter(user=user).order_by("-created_at")[:4]

    for goal in goals:
        if goal.target_amount and goal.target_amount != 0:
            percentage = (goal.current_amount / goal.target_amount) * 100
            goal.progress_percentage = min(percentage, 100)
        else:
            goal.progress_percentage = 0

    # ===== Debt Chart Data =====
    debts = Debt.objects.filter(user=user)
    debt_labels = json.dumps([d.title for d in debts])
    debt_totals = json.dumps([float(d.remaining_amount) for d in debts])

    # ===== Calculate REAL total balance =====
    # Start with UserProfile balance
    base_balance = profile.balance or 0

    # Total borrowed debts (money you owe)
    borrowed_debts = Debt.objects.filter(user=user, debt_type="borrowed").aggregate(total=Sum("remaining_amount"))["total"] or 0

    # Total lent debts (money others owe you)
    lent_debts = Debt.objects.filter(user=user, debt_type="lent").aggregate(total=Sum("remaining_amount"))["total"] or 0

    # Total money allocated to goals (optional, to subtract if you consider them "reserved")
    allocated_goals = Goal.objects.filter(user=user).aggregate(total=Sum("current_amount"))["total"] or 0

    # Real total balance
    total_balance = base_balance - expense - borrowed_debts + lent_debts - allocated_goals

    context = {
        "profile": profile,
        "balance": total_balance,
        "income": income,
        "expense": expense,
        "saved": saved,
        "today_count": today_count,
        "monthly_expense": monthly_expense,
        "budget": budget,
        "goals":goals,
        "budget_left": budget_left,
        "category_expenses": category_expenses,
        "category_labels": category_labels,
        "category_totals": category_totals,
        "transactions": recent_transactions,
        "debt_labels": debt_labels,
        "debt_totals": debt_totals,
        "income_cat_labels": income_cat_labels,
        "income_cat_totals": income_cat_totals,
        "expense_cat_labels": expense_cat_labels,
        "expense_cat_totals": expense_cat_totals,
    }

    return render(request, "fintrack_app/dashboard.html", context)


class UserBaseView(LoginRequiredMixin):
    fields = []           
    success_url = None   

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class CategoryListView(UserBaseView, ListView):
    model = Category
    template_name = 'fintrack_app/category/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(UserBaseView, CreateView):
    model = Category
    fields = ['name', 'category_type']
    template_name = 'fintrack_app/category/category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(CategoryCreateView, UpdateView):
    template_name = 'fintrack_app/category/category_form.html'


class CategoryDeleteView(UserBaseView, DeleteView):
    model = Category
    template_name = 'fintrack_app/category/category_delete.html'
    success_url = reverse_lazy('category-list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class TransactionListView(UserBaseView, ListView):
    model = Transaction
    template_name = 'fintrack_app/transaction/transaction_list.html'
    context_object_name = 'transactions'


class TransactionCreateView(UserBaseView, CreateView):
    model = Transaction
    fields = ['category', 'transaction_type', 'amount', 'note']
    template_name = 'fintrack_app/transaction/transaction_form.html'
    success_url = reverse_lazy('transaction-list')


class TransactionUpdateView(TransactionCreateView, UpdateView):
    template_name = 'fintrack_app/transaction/transaction_form.html'


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'fintrack_app/transaction/transaction_delete.html'
    success_url = reverse_lazy('transaction-list')

class BudgetListView(UserBaseView, ListView):
    model = Budget
    template_name = 'fintrack_app/budget/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class BudgetCreateView(UserBaseView, CreateView):
    model = Budget
    fields = ['monthly_limit', 'month']
    template_name = 'fintrack_app/budget/budget_form.html'
    success_url = reverse_lazy('budget-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BudgetUpdateView(BudgetCreateView, UpdateView):
    template_name = 'fintrack_app/budget/budget_form.html'

class BudgetDeleteView(UserBaseView, DeleteView):
    model = Budget
    template_name = 'fintrack_app/budget/budget_delete.html'
    success_url = reverse_lazy('budget-list')

class DebtListView(UserBaseView, ListView):
    model = Debt
    template_name = 'fintrack_app/debt/debt_list.html'
    context_object_name = 'debts'

class DebtCreateView(UserBaseView, CreateView):
    model = Debt
    fields = ['title', 'debt_type', 'total_amount', 'remaining_amount',
              'start_date', 'due_date', 'note']
    template_name = 'fintrack_app/debt/debt_form.html'
    success_url = reverse_lazy('debt-list')


class DebtUpdateView(DebtCreateView, UpdateView):
    template_name = 'fintrack_app/debt/debt_form.html'


class DebtDeleteView(UserBaseView, DeleteView):
    model = Debt
    template_name = 'fintrack_app/debt/debt_delete.html'
    success_url = reverse_lazy('debt-list')

class GoalListView(UserBaseView, ListView):
    model = Goal
    template_name = 'fintrack_app/goal/goal_list.html'
    context_object_name = 'goals'

def allocate_goal_money(user_profile, amount, source=None):
    if user_profile.balance < amount:
        raise ValueError("Not enough balance.")

    user_profile.balance -= amount
    user_profile.save()
    
class GoalCreateView(UserBaseView, CreateView):
    model = Goal
    fields = ['title', 'goal_type', 'target_amount', 'current_amount', 'deadline']
    template_name = 'fintrack_app/goal/goal_form.html'
    success_url = reverse_lazy('goal-list')
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('current_amount', 0)
        user_profile = self.request.user.userprofile
        source = self.request.POST.get('source', 'total')

        if amount > 0:
            try:
                allocate_goal_money(user_profile, amount, source)
            except ValueError as e:
                form.add_error('current_amount', str(e))
                return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalUpdateView(UserBaseView, UpdateView):
    model = Goal
    fields = ['title', 'goal_type', 'target_amount', 'current_amount', 'deadline']
    template_name = 'fintrack_app/goal/goal_form.html'
    success_url = reverse_lazy('goal-list')
    
    def form_valid(self, form):
        goal = self.get_object()
        user_profile = self.request.user.userprofile

        old_amount = goal.current_amount
        new_amount = form.cleaned_data.get('current_amount', 0)
        diff = new_amount - old_amount

        if diff > 0:
            source = self.request.POST.get('source', 'total')
            try:
                allocate_goal_money(user_profile, diff, source)
            except ValueError as e:
                form.add_error('current_amount', str(e))
                return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalDeleteView(UserBaseView, DeleteView):
    model = Goal
    template_name = 'fintrack_app/goal/goal_confirm_delete.html'
    success_url = reverse_lazy('goal-list')

