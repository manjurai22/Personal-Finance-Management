from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import UserProfile, Category, Transaction, Budget, Debt, Goal, Report

# Create your views here.
def dashboard(request):
    user = request.user

    profile = get_object_or_404(UserProfile, user=user)
    total_balance = profile.total_balance()

    income = Transaction.objects.filter(user=user, transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
    expense = Transaction.objects.filter(user=user, transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0

    category_expenses = (
        Transaction.objects.filter(user=user, transaction_type='expense')
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    goals = Goal.objects.filter(user=user).order_by('-created_at')[:5]
    debts = Debt.objects.filter(user=user).order_by('-start_date')[:5]

    context = {
        'profile': profile,
        'income': income,
        'expense': expense,
        'balance': total_balance,
        'category_expenses': category_expenses,
        'goals': goals,
        'debts': debts,
    }
    return render(request, 'dashboard.html', context)

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
