import os
import time
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories"
    )
    name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Shop(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shops"
    )

    name = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Expense(models.Model):

    def expense_bill_upload_path(instance, filename):
        ext = filename.split('.')[-1]
        timestamp = int(time.time() * 1000)
        new_filename = f"bill_{instance.user.id}_{timestamp}.{ext}"
        return os.path.join("bills", new_filename)

    def validate_bill_file(value):
        ext = value.name.split('.')[-1].lower()
        allowed = ['jpg', 'jpeg', 'png', 'pdf']

        if ext not in allowed:
            raise ValidationError("Only JPG, PNG or PDF files allowed.")

        if value.size > 5 * 1024 * 1024:
            raise ValidationError("File size must be under 5MB.")


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expenses"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="expenses"
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    date = models.DateField(default=timezone.now)

    description = models.TextField(
        blank=True
    )

    bill = models.FileField(
        upload_to=expense_bill_upload_path,
        validators=[validate_bill_file],
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.amount} - {self.category}"

    def delete(self, *args, **kwargs):
        if self.bill:
            self.bill.delete(save=False)
        super().delete(*args, **kwargs)


