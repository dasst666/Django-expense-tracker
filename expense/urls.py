from django.urls import path
from . import views

app_name = 'expense'

urlpatterns = [
    path("", views.ExpenseListView.as_view(), name="expense_list"),
    path("add/", views.ExpenseCreateView.as_view(), name="expense_add"),
    path("add_expense_category/", views.ExpenseCategoryCreateView.as_view(), name="expense_category_add"),
    path("delete/<int:pk>/", views.ExpenseDeleteView.as_view(), name="expense_delete"),
    path("update/<int:pk>/", views.ExpenseUpdateView.as_view(), name="expense_update"),
    path("category_pie/", views.ExpenseCategoryPieView.as_view(), name="expense_category_pie"),
    path("monthly/", views.ExpenseMonthlyView.as_view(), name="expense_monthly"),
]
