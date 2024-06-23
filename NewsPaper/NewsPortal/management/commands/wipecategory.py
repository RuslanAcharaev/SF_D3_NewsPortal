from django.core.management.base import BaseCommand, CommandError
from NewsPortal.models import *


class Command(BaseCommand):
    help = 'Удаляет публикации в выбранной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? (да/нет) ')

        if answer != 'да':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(postCategory=category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Успешно удалены все новости из категории "{category.name}"'))

        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не удалось найти заданную категорию'))
