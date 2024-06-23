from django.urls import path
# Импортируем созданное нами представление
from .views import (
   PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, user_promotion, CategoryListView, subscribe,
   unsubscribe, SubscriptionsList,
)
from django.views.decorators.cache import cache_page

urlpatterns = [
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60)(PostList.as_view()), name='post_list'),
   # pk — это первичный ключ новости, которая будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('posts/search/', PostSearch.as_view(), name='post_search'),
   path('posts/news/create/', PostCreate.as_view(), name='news_create'),
   path('posts/articles/create/', PostCreate.as_view(), name='articles_create'),
   path('posts/news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
   path('posts/articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_update'),
   path('posts/news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('posts/articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('posts/promote/', user_promotion, name='user_promotion'),
   path('subscriptions/', SubscriptionsList.as_view(), name='subscriptions'),
   path('posts/categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('posts/categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
   path('posts/categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
]
