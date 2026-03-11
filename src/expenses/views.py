from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from expenses.models import Category
from expenses.forms import CategoryForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "expenses/dashboard.html"
    login_url = "accounts:request_otp"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context.update({
            "user": user,
        })

        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "expenses/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryListAjaxView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')

        qs = Category.objects.filter(user=request.user)

        # Search filter
        if search_value:
            qs = qs.filter(name__icontains=search_value)

        total_records = Category.objects.filter(user=request.user).count()
        filtered_records = qs.count()

        # Optional: Sorting
        order_col_index = int(request.GET.get('order[0][column]', 1))
        order_dir = request.GET.get('order[0][dir]', 'asc')
        columns = ['id', 'name', 'created_at']
        order_column = columns[order_col_index]
        if order_dir == 'desc':
            order_column = '-' + order_column
        qs = qs.order_by(order_column)

        # Pagination
        qs = qs[start:start + length]

        data = []
        for cat in qs:
            # URLs for update and delete
            update_url = reverse('expenses:category_update', args=[cat.id])
            delete_url = reverse('expenses:category_delete', args=[cat.id])

            data.append({
                'name': cat.name,
                'created_at': timezone.localtime(cat.created_at).strftime("%d %b %Y %H:%M"),
                'action': f'''
                    <a href="{update_url}" class="btn btn-sm btn-primary" title="Edit">
                        <i class="fas fa-edit"></i>
                    </a>
                    <button type="button" class="btn btn-sm btn-danger delete-btn" data-url="{delete_url}" data-name="{cat.name}" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                '''
            })

        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        })


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "expenses/category_form.html"
    success_url = reverse_lazy("expenses:category_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Category "{form.instance.name}" added successfully!')
        return response

    def form_invalid(self, form):
        form.instance.user = self.request.user
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.user = self.request.user
        return form

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "expenses/category_form.html"
    success_url = reverse_lazy("expenses:category_list")

    def get_queryset(self):
        # Ensure user can only update their own categories
        return Category.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Category "{form.instance.name}" updated successfully!')
        return response

    def form_invalid(self, form):
        form.instance.user = self.request.user
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.instance.user = self.request.user
        return form


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        name = self.object.name
        self.object.delete()

        return JsonResponse({
            "success": True,
            "message": f'{name} deleted successfully'
        })