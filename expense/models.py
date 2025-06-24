from django.db import models
from django.utils import timezone
from django.conf import settings

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name_plural = 'Категории трат'

    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})
    

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.amount} {self.category} {self.date}'
    
    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['-date'])
            ]
        verbose_name = 'Траты'
        verbose_name_plural = 'Траты'
    
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})

class ExpenseCategoryLimit(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, related_name='limits')
    month = models.DateField()
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['category', 'month']
    
    def __str__(self):
        return f"{self.category.name} - {self.month}: {self.limit}"
    