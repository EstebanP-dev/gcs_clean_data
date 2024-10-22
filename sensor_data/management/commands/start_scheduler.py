from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BlockingScheduler

from ...services import generate_and_insert_sensor_data

class Command(BaseCommand):
    help = 'Inicia el programador para insertar datos en intervalos regulares'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=3, help='Intervalo en segundos entre inserciones de datos')

    def handle(self, *args, **options):
        interval = options['interval']
        self.stdout.write(f'Iniciando el programador con un intervalo de {interval} segundos')
        scheduler = BlockingScheduler()

        scheduler.add_job(generate_and_insert_sensor_data, 'interval', seconds=interval)

        try:
            scheduler.start()
        except KeyboardInterrupt:
            self.stdout.write('Programador detenido.')
            scheduler.shutdown()