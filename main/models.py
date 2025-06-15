from django.db import models
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name']),]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args={self.slug})
    

class Transaction(models.Model):
    category = models.ForeignKey(Category, related_name='transactions', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    created = models.DateTimeField(default=timezone.now)

    INCOME_TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]
    income_type = models.CharField(max_length=10, 
                                    choices=INCOME_TYPE_CHOICES, 
                                    default='expense')


    class Meta:
        ordering = ['name']
        indexes = [
            # models.Index(fields=['id, slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:transaction_detail", kwargs={"pk": self.pk})

