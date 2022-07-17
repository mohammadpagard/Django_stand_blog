from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='نام کاربری')
    father_name = models.CharField(max_length=25, verbose_name='نام پدر')
    melicode = models.CharField(max_length=10, verbose_name='کد ملی')
    image = models.ImageField(upload_to='profile/images', null=True, blank=True, verbose_name='عکس')


    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حساب های کاربری'

    def __str__(self):
        return self.user.username
