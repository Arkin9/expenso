from django.urls import path
from .views import DashboardView, CategoryListView, CategoryListAjaxView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView


app_name = "expenses"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/datatables/", CategoryListAjaxView.as_view(), name="category_datatable"),
    path("categories/add/", CategoryCreateView.as_view(), name="category_add"),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]