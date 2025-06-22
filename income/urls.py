from django.urls import path
from . import views

app_name = 'income'

urlpatterns = [
    path("", views.IncomeListView.as_view(), name="income_list"),
    path("add/", views.IncomeCreateView.as_view(), name="income_add"),
    path("add_income_category/", views.IncomeCategoryCreateView.as_view(), name="income_category_add"),
    path("delete/<int:pk>/", views.IncomeDeleteView.as_view(), name="income_delete"),
    path("update/<int:pk>/", views.IncomeUpdateView.as_view(), name="income_update"),
    path("monthly/", views.IncomeMonthlyView.as_view(), name="income_monthly"),
]
