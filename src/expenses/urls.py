from django.urls import path
from .views import DashboardView, CategoryListView, CategoryListAjaxView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, ShopListView, ShopListAjaxView, ShopCreateView, ShopUpdateView, ShopDeleteView, ExpenseListView, ExpenseListAjaxView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView


app_name = 'expenses'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/datatables/', CategoryListAjaxView.as_view(), name='category_datatable'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('shops/', ShopListView.as_view(), name='shop_list'),
    path('shops/datatables/', ShopListAjaxView.as_view(), name='shop_datatable'),
    path('shops/add/', ShopCreateView.as_view(), name='shop_add'),
    path('shops/<int:pk>/update/', ShopUpdateView.as_view(), name='shop_update'),
    path('shops/<int:pk>/delete/', ShopDeleteView.as_view(), name='shop_delete'),
    path('expenses/', ExpenseListView.as_view(), name='expense_list'),
    path('expenses/datatables/', ExpenseListAjaxView.as_view(), name='expense_datatable'),
    path('expenses/add/', ExpenseCreateView.as_view(), name='expense_add'),
    path('expenses/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense_update'),
    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),

]