from django.db import models
from django.contrib.auth.models import AbstractUser
import pytz
from datetime import datetime, timedelta
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='Аватар')
    avatar_url = models.CharField(max_length=128, blank=True, null=True)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст')

    activate_key = models.CharField(max_length=128, verbose_name='Ключ активации', blank=True, null=True)
    activate_key_expired = models.DateTimeField(blank=True, null=True)

    def is_activate_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activate_key_expired + timedelta(hours=48):
            return True
        return False

class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    OTHERS = 'O'

    GENDERS = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
        (OTHERS, 'И'),
    )

    user = models.OneToOneField(ShopUser, null=False, unique=True, on_delete=models.CASCADE, db_index=True)
    tagline = models.CharField(max_length=128, verbose_name='Тэги', blank=True)
    about_me = models.TextField(verbose_name='Обо мне')
    gender = models.CharField(choices=GENDERS, default=OTHERS, verbose_name='Пол', max_length=1)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def update_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
