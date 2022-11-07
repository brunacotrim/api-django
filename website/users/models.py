from django.db import models


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(Base):
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
    
    def __str__(self):
        return self.username