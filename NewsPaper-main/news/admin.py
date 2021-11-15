from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, Subscriber


# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = [field.name for field in Post._meta.get_fields()]
    list_filter = [field.name for field in Post._meta.get_fields()]
    search_fields = [field.name for field in Post._meta.get_fields()]

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscriber)
