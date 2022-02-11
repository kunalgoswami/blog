from django.contrib import admin
from .models import Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'desc','user']


admin.site.register(Post, PostAdmin)
