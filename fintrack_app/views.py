from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import UserProfile, Category, Transaction, Budget, Debt, Goal
from datetime import date
import json
# Create your views here.
def dashboard(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

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
    today_count = transactions.filter(
        date=today
    ).count()

    # ===== Monthly Expense =====
    monthly_expense = transactions.filter(
        transaction_type="expense",
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum("amount"))["total"] or 0

    # ===== Monthly Budget =====
    budget = Budget.objects.filter(
        user=user,
        month__year=today.year,
        month__month=today.month,
    ).aggregate(total=Sum("monthly_limit"))["total"] or 0

    budget_left = budget - monthly_expense

    # ===== Category Expenses =====
    category_expenses = transactions.filter(
        transaction_type="expense"
    ).values("category__name").annotate(
        total=Sum("amount")
    )

    # ===== Recent Transactions =====
    recent_transactions = transactions.select_related(
        "category"
    ).order_by("-date")[:8]

    category_labels = json.dumps(
        [c["category__name"] for c in category_expenses]
    )

    category_totals = json.dumps(
       [float(c["total"]) for c in category_expenses]
     )
    
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


    context = {
        "profile": profile,
        "balance": profile.total_balance(),
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
    fields = ['category', 'transaction_type', 'payment_source', 'amount', 'date', 'note']
    template_name = 'fintrack_app/transaction/transaction_form.html'
    success_url = reverse_lazy('transaction-list')


class TransactionUpdateView(TransactionCreateView, UpdateView):
    template_name = 'fintrack_app/transaction/transaction_form.html'


class TransactionDeleteView(UserBaseView, DeleteView):
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
    fields = ['monthly_limit', 'month', 'year']
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

def allocate_goal_money(user_profile, amount, source):
    if source == 'total':
        if user_profile.total_balance < amount:
            raise ValueError("Not enough total balance.")
        user_profile.total_balance -= amount

    elif source == 'card':
        if user_profile.card_balance < amount:
            raise ValueError("Not enough card balance.")
        user_profile.card_balance -= amount

    elif source == 'e_wallet':
        if user_profile.e_wallet < amount:
            raise ValueError("Not enough e-wallet balance.")
        user_profile.e_wallet -= amount

    else:
        raise ValueError("Invalid source selected.")
    
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

