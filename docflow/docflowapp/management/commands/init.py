from django.core.management.base import BaseCommand
from docflowapp.models import DocumentType, Classifier


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Выбираем ВСЕ категории

        obj_contract = None
        obj_order = None

        count = DocumentType.objects.count()

        if count == 0:
            print('Создание списка типов документа')
            DocumentType.objects.create(name='Договор')
            DocumentType.objects.create(name='Дополнительное соглашение')
            DocumentType.objects.create(name='Приложение')
            DocumentType.objects.create(name='Акт')

            DocumentType.objects.create(name='Приказ')
            DocumentType.objects.create(name='Распоряжение')

            DocumentType.objects.create(name='Исходящий')
            DocumentType.objects.create(name='Входящий')
            DocumentType.objects.create(name='Внутренний')

            DocumentType.objects.create(name='Счет')

        else:
            print('Типы документов уже заполнены')

        obj_contract = DocumentType.objects.get(name='Договор')
        obj_order = DocumentType.objects.get(name='Приказ')

        count = Classifier.objects.count()
        if count == 0:
            if obj_contract:
                print('Создание классификатора для договоров')
                obj = Classifier.objects.create(name='Хозяйственный')
                obj.document_type.add(obj_contract)
                obj = Classifier.objects.create(name='Аудивидуальное произведение')
                obj.document_type.add(obj_contract)

            if obj_order:
                print('Создание классификатора для приказов')
                obj = Classifier.objects.create(name='По личному соcтаву')
                obj.document_type.add(obj_order)
                obj = Classifier.objects.create(name='О запуске в производство')
                obj.document_type.add(obj_order)
        else:
            print('классификатор уже заполнен')
