from django.core.management.base import BaseCommand
from account.models import User, MonthlyPayment
from datetime import datetime


class Command(BaseCommand):
    help = 'Bütün istifadəçilər üçün cari il üçün 12 ayın ödəniş qeydlərini yaradır'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=int,
            help='İl (default: cari il)',
            default=datetime.now().year
        )

    def handle(self, *args, **options):
        year = options['year']
        current_year = datetime.now().year
        
        if year != current_year:
            self.stdout.write(
                self.style.WARNING(
                    f'Diqqət: {year} ili üçün qeydlər yaradılır. Cari il {current_year}-dir.'
                )
            )
        
        users = User.objects.all()
        created_count = 0
        existing_count = 0
        
        for user in users:
            for month in range(1, 13):
                payment, created = MonthlyPayment.objects.get_or_create(
                    user=user,
                    month=month,
                    year=year,
                    defaults={'is_paid': False}
                )
                if created:
                    created_count += 1
                else:
                    existing_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Uğurla tamamlandı!\n'
                f'{year} ili üçün:\n'
                f'- Yeni qeydlər: {created_count}\n'
                f'- Mövcud qeydlər: {existing_count}\n'
                f'- Ümumi istifadəçi sayı: {users.count()}'
            )
        )
