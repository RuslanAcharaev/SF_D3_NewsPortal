from django.contrib import admin
from .models import Post, PostCategory, Category, Author, Comment, Subscriber
from modeltranslation.admin import TranslationAdmin # импортируем модель админки


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с новостями
    list_display = ('title', 'author', 'dateCreation', 'rating')
    list_filter = ('title', 'postCategory', 'author', 'dateCreation', 'rating')
    search_fields = ('title', 'postCategory__name')


class PostTranslation(TranslationAdmin):
    model = Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


class CategoryTranslation(TranslationAdmin):
    model = Category


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Subscriber)
