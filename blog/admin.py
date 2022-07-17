from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "show_image")
    list_editable = ("status",)
    list_filter = ("author", "status", "publish")
    search_fields = ("title", "body")
    exclude = ("slug", "created", "publish")



admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.Message)
admin.site.register(models.Like)
