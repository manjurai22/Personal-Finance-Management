from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-add'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='transaction-add'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction-edit'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction-delete'),

    path('budgets/', views.BudgetListView.as_view(), name='budget-list'),
    path('budgets/add/', views.BudgetCreateView.as_view(), name='budget-add'),
    path('budgets/<int:pk>/edit/', views.BudgetUpdateView.as_view(), name='budget-edit'),
    path('budgets/<int:pk>/delete/', views.BudgetDeleteView.as_view(), name='budget-delete'),

    path('goals/', views.GoalListView.as_view(), name='goal-list'),
    path('goals/add/', views.GoalCreateView.as_view(), name='goal-add'),
    path('goals/<int:pk>/edit/', views.GoalUpdateView.as_view(), name='goal-edit'),
    path('goals/<int:pk>/delete/', views.GoalDeleteView.as_view(), name='goal-delete'),

    path("debts/", views.DebtListView.as_view(), name="debt-list"),
    path("debts/add/", views.DebtCreateView.as_view(), name="debt-add"),
    path("debts/<int:pk>/edit/", views.DebtUpdateView.as_view(), name="debt-edit"),
    path("debts/<int:pk>/delete/", views.DebtDeleteView.as_view(), name="debt-delete"),

]

