from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Product(Base):
    sku = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=60)
    ean = models.IntegerField(blank=True)
    description = models.TextField(blank=True)
    brand = models.CharField(blank=True, max_length=25)
    warranty_time = models.IntegerField(blank=True)
    height = models.DecimalField(decimal_places=3, max_digits=7)
    width = models.DecimalField(decimal_places=3, max_digits=7)
    length = models.DecimalField(decimal_places=3, max_digits=7)
    weight = models.DecimalField(decimal_places=3, max_digits=7)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    special_price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['id']
    
    def __str__(self):
        return self.name