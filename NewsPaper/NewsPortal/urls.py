from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, user_promotion


urlpatterns = [
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name='post_list'),
   # pk — это первичный ключ новости, которая будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
   path('promote/', user_promotion, name='user_promotion'),
]
