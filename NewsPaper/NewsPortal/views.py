# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


# Переопределяем миксин PermissionRequiredMixin для проверки авторства
class OwnerPermissionRequiredMixin(PermissionRequiredMixin):
    def has_permission(self):
        perms = self.get_permission_required()
        if not self.get_object().author.authorUser == self.request.user:
            raise PermissionDenied()
        return self.request.user.has_perms(perms)


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    # Указываем количество записей на странице:
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    # Указываем количество записей на странице:
    paginate_by = 10

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список новостей
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — piece_of_news.html
    template_name = 'piece_of_news.html'
    # Название объекта, в котором будет выбранная пользователем новость
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    # Настраиваем проверку прав
    permission_required = ('NewsPortal.add_post',)
    # Настраиваем выдачу ошибки с 403 кодом
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель новостей
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        form.instance.author = self.request.user.author
        if self.request.path == '/posts/articles/create/':
            post.categoryType = 'AR'
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostUpdate(OwnerPermissionRequiredMixin, UpdateView):
    # Настраиваем проверку прав
    permission_required = ('NewsPortal.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}
        if self.request.path == f'/posts/news/{post.pk}/edit/' and post.categoryType != 'NW':
            return redirect(f'/posts/articles/{post.pk}/edit/', context=context)
        elif self.request.path == f'/posts/articles/{post.pk}/edit/' and post.categoryType != 'AR':
            return redirect(f'/posts/news/{post.pk}/edit/', context=context)
        return super(PostUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostDelete(OwnerPermissionRequiredMixin, DeleteView):
    # Настраиваем проверку прав
    permission_required = ('NewsPortal.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        context = {'post_id': post.pk}
        if self.request.path == f'/posts/news/{post.pk}/delete/' and post.categoryType != 'NW':
            return redirect(f'/posts/articles/{post.pk}/delete/', context=context)
        elif self.request.path == f'/posts/articles/{post.pk}/delete/' and post.categoryType != 'AR':
            return redirect(f'/posts/news/{post.pk}/delete/', context=context)
        return super(PostDelete, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


# Добавляем возможность пользователю перейти в группу authors
@login_required
def user_promotion(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        group.user_set.add(user)
        Author.objects.create(authorUser=user)
    return redirect('/posts/')
