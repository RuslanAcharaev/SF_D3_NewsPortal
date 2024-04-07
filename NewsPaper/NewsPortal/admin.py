from django.contrib import admin
from .models import Post, PostCategory, Category, Author, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
