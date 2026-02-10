from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import UserProfile, Category, Transaction, Budget, Debt, Goal, Report
from django.db.models.functions import TruncMonth
from datetime import date
# Create your views here.
def dashboard(request):
    user = request.user

    profile = get_object_or_404(UserProfile, user=user)
    total_balance = profile.total_balance()

    income = (
        Transaction.objects
        .filter(user=user, transaction_type="income")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    expense = (
        Transaction.objects
        .filter(user=user, transaction_type="expense")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    transactions = (
        Transaction.objects
        .filter(user=user)
        .select_related("category")
        .order_by("-date")[:8]
    )

    category_expenses = (
        Transaction.objects
        .filter(user=user, transaction_type="expense")
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    monthly_expenses = (
        Transaction.objects
        .filter(user=user, transaction_type="expense")
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    monthly_labels = [
        m["month"].strftime("%b %Y") for m in monthly_expenses
    ]
    monthly_totals = [
        float(m["total"]) for m in monthly_expenses
    ]

    goals = Goal.objects.filter(user=user).order_by("-created_at")[:4]
    debts = Debt.objects.filter(user=user).order_by("-start_date")[:4]

    context = {
        "profile": profile,
        "balance": total_balance,
        "income": income,
        "expense": expense,
        "transactions": transactions,
        "monthly_labels": monthly_labels,
        "monthly_totals": monthly_totals,
        "category_expenses": category_expenses,
        "goals": goals,
        "debts": debts,
    }

    return render(request, "fintrack_app/dashboard.html", context)




class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'category_type']
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'category_type']
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transaction/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['category', 'transaction_type', 'payment_source', 'amount', 'date', 'note']
    template_name = 'transaction/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['category', 'transaction_type', 'payment_source', 'amount', 'date', 'note']
    template_name = 'transaction/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transaction/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction-list')

class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'budget/budget_list.html'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    fields = ['category', 'monthly_limit', 'month']
    template_name = 'budget/budget_form.html'
    success_url = reverse_lazy('budget-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    fields = ['category', 'monthly_limit', 'month']
    template_name = 'budget/budget_form.html'
    success_url = reverse_lazy('budget-list')

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'budget/budget_confirm_delete.html'
    success_url = reverse_lazy('budget-list')

class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'goal/goal_list.html'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    fields = ['title', 'goal_type', 'target_amount', 'current_amount', 'deadline']
    template_name = 'goal/goal_form.html'
    success_url = reverse_lazy('goal-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    fields = ['title', 'goal_type', 'target_amount', 'current_amount', 'deadline']
    template_name = 'goal/goal_form.html'
    success_url = reverse_lazy('goal-list')

class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'goal/goal_confirm_delete.html'
    success_url = reverse_lazy('goal-list')

class DebtListView(LoginRequiredMixin, ListView):
    model = Debt
    template_name = 'debt/debt_list.html'
    context_object_name = 'debts'

    def get_queryset(self):
        return Debt.objects.filter(user=self.request.user)

class DebtCreateView(LoginRequiredMixin, CreateView):
    model = Debt
    fields = ['title', 'debt_type', 'total_amount', 'remaining_amount', 'start_date', 'due_date', 'note']
    template_name = 'debt/debt_form.html'
    success_url = reverse_lazy('debt-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DebtUpdateView(LoginRequiredMixin, UpdateView):
    model = Debt
    fields = ['title', 'debt_type', 'total_amount', 'remaining_amount', 'start_date', 'due_date', 'note']
    template_name = 'debt/debt_form.html'
    success_url = reverse_lazy('debt-list')

class DebtDeleteView(LoginRequiredMixin, DeleteView):
    model = Debt
    template_name = 'debt/debt_confirm_delete.html'
    success_url = reverse_lazy('debt-list')

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'report/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.filter(user=self.request.user).order_by('-created_at')

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    fields = ['report_type', 'start_date', 'end_date']
    template_name = 'report/report_form.html'
    success_url = reverse_lazy('report-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def allocate_goal_money(user_profile, goal, amount, source):
    """
    Deduct amount from chosen source and move to reserved balance.
    source: 'total', 'card', 'e_wallet'
    """
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

    # Add to reserved balance
    user_profile.reserved_balance += amount
    user_profile.save()

    # Update goal
    goal.current_amount += amount
    goal.save()

class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'goal/goal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    fields = ['title', 'goal_type', 'target_amount', 'current_amount', 'deadline']
    template_name = 'goal/goal_form.html'
    success_url = reverse_lazy('goal-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Allocate money if user wants (choose source via a POST param or field)
        amount = form.instance.current_amount
        if amount > 0:
            user_profile = self.request.user.userprofile
            source = self.request.POST.get('source', 'total')  # Default to total_balance

            try:
                allocate_goal_money(user_profile, form.instance, amount, source)
            except ValueError as e:
                form.add_error('current_amount', str(e))
                return self.form_invalid(form)

        return response


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    fields = ['title', 'goal_type', 'target_amount', 'current_amount', 'deadline']
    template_name = 'goal/goal_form.html'
    success_url = reverse_lazy('goal-list')

    def form_valid(self, form):
        goal = form.instance
        user_profile = self.request.user.userprofile

        # Calculate increase in current_amount
        old_goal = Goal.objects.get(pk=goal.pk)
        diff = form.cleaned_data.get('current_amount', 0) - old_goal.current_amount

        if diff > 0:
            # Source can be chosen via a POST param again
            source = self.request.POST.get('source', 'total')
            try:
                allocate_goal_money(user_profile, goal, diff, source)
            except ValueError as e:
                form.add_error('current_amount', str(e))
                return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'goal/goal_confirm_delete.html'
    success_url = reverse_lazy('goal-list')
