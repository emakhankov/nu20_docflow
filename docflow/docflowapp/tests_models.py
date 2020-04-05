from django.test import TestCase
from mixer.backend.django import mixer
from faker import Faker

from .models import Document, Counterpart

# Create your tests here.
class DocFlowTestCase(TestCase):

    def setUp(self):
        self.document = mixer.blend(Document)
        #Для many to many не заполняется, поэтому их создадим

        self.counterpart1 = mixer.blend(Counterpart)
        self.counterpart2 = mixer.blend(Counterpart)
        self.counterpart3 = mixer.blend(Counterpart)


    def test_document_counterparts_zero(self):
        """
        Теституем что если контрагентов нет то и поле конкатенации пусто. Пустая строка это False
        """
        self.assertFalse(self.document.counterparts())

    def test_document_counterparts_one(self):
        """
        Теституем что если контрагент один то поле конкатенации равно имени этого контрагента
        """
        self.document.counterpart.add(self.counterpart1)
        self.assertEqual(self.document.counterparts(), self.counterpart1.name)

    def test_document_counterparts_mult(self):
        """
        Теституем что если контрагентов 3 то есть запятая и в конкатенации присутствуют названия этих контрагентов
        """
        self.document.counterpart.add(self.counterpart1, self.counterpart2, self.counterpart3)
        self.assertIn(',', self.document.counterparts())
        self.assertIn(self.counterpart1.name, self.document.counterparts())
        self.assertIn(self.counterpart2.name, self.document.counterparts())
        self.assertIn(self.counterpart3.name, self.document.counterparts())