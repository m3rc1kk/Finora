from django.db import models
from django.conf import settings

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_categories', null=True, blank=True)
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=7, default = '#FF0C59')
    is_system = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
