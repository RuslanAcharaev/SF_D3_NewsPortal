from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter
from .models import Post, Category
from django.forms import DateTimeInput


# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    # Переопределяем
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['title__iregex'].label = 'Заголовок содержит'

    postCategory = ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        conjoined=True,
    )

    created_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Новости позднее',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'title': ['iregex'],
        }
