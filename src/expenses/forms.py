from django import forms
from .models import Category, Shop, Expense


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Category name"
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        user = self.instance.user

        if Category.objects.filter(user=user, name__iexact=name).exists():
            raise forms.ValidationError("You already have a category with this name.")

        return name


class ShopForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Shop name"
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        user = self.instance.user

        if Shop.objects.filter(user=user, name__iexact=name).exists():
            raise forms.ValidationError("You already have a shop with this name.")

        return name


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = [
            "category",
            "shop",
            "amount",
            "date",
            "description",
            "bill",
        ]

        widgets = {
            "category": forms.Select(attrs={
                "class": "form-select"
            }),

            "shop": forms.Select(attrs={
                "class": "form-select"
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Amount"
            }),

            "date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Optional description"
            }),

            "bill": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": ".jpg,.jpeg,.png,.pdf"
            })
        }