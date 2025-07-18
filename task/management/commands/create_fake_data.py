import random

from django.core.management import BaseCommand
from faker import Faker

from account.models import User
from task.models import Task


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.faker = Faker(locale='fa_IR')

    def handle(self, *args, **options):
        user = User.objects.get_or_create(email='example@example.com', is_active=True, password="zxc_123#ddd")[0]
        for _ in range(5):
            task = Task.objects.create(
                content=self.faker.text(max_nb_chars=200),
                is_complete=random.choice([True, False]),
                user=user
            )
