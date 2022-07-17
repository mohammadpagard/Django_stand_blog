from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _



class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان'))
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name=_('لینک'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ساخت'))


    class Meta:
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name=_('نویسنده'))
    title = models.CharField(max_length=50, unique_for_date="publish", verbose_name=_('عنوان'))
    slug = models.SlugField(null=True, unique=True, blank=True, verbose_name=_('لینک'))
    category = models.ManyToManyField(Category, related_name='posts', verbose_name=_('دسته بندی'))
    body = models.TextField(verbose_name=_('محتوا'))
    image = models.ImageField(verbose_name=_('عکس'), upload_to='images/posts', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ساخت'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('آخرین بروزرسانی'))
    publish = models.DateTimeField(default=timezone.now, verbose_name=_('زمان انتشار'))
    status = models.BooleanField(default=True, verbose_name=_('وضعیت'))


    class Meta:
        verbose_name = _('مقاله')
        verbose_name_plural = _('مقاله ها')

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    # show image in admin panel
    def show_image(self):
        if self.image:
            return format_html(
                f'<img src="{self.image.url}" width="60px" height="60px"'
            )
        return format_html('<h3 style="color: brown">تصویر ندارد</h3>')


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.body[:10]}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('مقاله'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name=_('کاربر'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name=_('پاسخ به'))
    body = models.TextField(verbose_name=_('عنوان'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ساخت'))


    class Meta:
        verbose_name = _('دیدگاه')
        verbose_name_plural = _('دیدگاه ها')


    def __str__(self):
        return self.body[:50]



class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('عنوان پیام'))
    text = models.TextField(verbose_name=_('محتوای پیام'))
    email = models.EmailField(verbose_name=_('ایمیل'))
    age = models.IntegerField(default=0, verbose_name=_('سن'))
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_('تاریخ ارسال پیام'))
    date = models.DateTimeField(default=timezone.now(), verbose_name=_('زمان پیام'))


    class Meta:
        verbose_name = _('پیام')
        verbose_name_plural = _('پیام ها')

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name=_('کاربر'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name=_('مقاله'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('لایک')
        verbose_name_plural = _('لایک ها')
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"