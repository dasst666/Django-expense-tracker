from django.db import models
from django.utils import timezone
from django.conf import settings


class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Income Categories'


class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE, related_name='incomes')
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.amount} {self.category} {self.date}'
    
    class Meta:
        ordering = ['-date']