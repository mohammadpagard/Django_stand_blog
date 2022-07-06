from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.html import format_html



class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name='نویسنده')
    title = models.CharField(max_length=50, unique_for_date="publish", verbose_name='عنوان')
    slug = models.SlugField(null=True, unique=True, blank=True, verbose_name='لینک')
    category = models.ManyToManyField(Category, related_name='posts', verbose_name='دسته بندی')
    body = models.TextField(verbose_name='محتوا')
    image = models.ImageField(verbose_name='عکس', upload_to='images/posts', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت')
    updated = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    status = models.BooleanField(default=True, verbose_name='وضعیت')


    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها'

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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'


    def __str__(self):
        return self.body[:50]



class Message(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    email = models.EmailField()
    age = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    date = models.DateTimeField(default=timezone.now())


    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return self.title

