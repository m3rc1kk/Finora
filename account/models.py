from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


def user_directory_path(instance, filename):
    return f'{instance.username}/profile_avatars/{filename}'

class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('profile', args = [self.id])

