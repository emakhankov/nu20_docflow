from django.test import Client
from django.test import TestCase
from mixer.backend.django import mixer
from faker import Faker

from .models import Counterpart, Classifier, DocumentType, Document
from usersapp.models import DocFlowUser


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.fake = Faker()
        self.user1 = DocFlowUser.objects.create_user(username='test_user1', email='test1@test.com', password='12345',
                                                     can_add_documents=False, can_find_documents=False)
        self.user2 = DocFlowUser.objects.create_user(username='test_user2', email='test1@test.com', password='12345',
                                                     can_add_documents=True, can_find_documents=False)
        self.user3 = DocFlowUser.objects.create_user(username='test_user3', email='test1@test.com', password='12345',
                                                     can_add_documents=False, can_find_documents=True)
        self.user4 = DocFlowUser.objects.create_user(username='test_user4', email='test1@test.com', password='12345',
                                                     can_add_documents=True, can_find_documents=True)


    def test_login_required(self):

        """
        Должен при входе перебрасывать на страницу авториации
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login(self):

        """
        При логине заходим на страницу
        """
        self.client.login(username='test_user1', password='12345')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_document_not_authorize(self):

        """
        Нужно специальное право чтобы регистрировать документы
        """
        self.client.login(username='test_user1', password='12345')
        response = self.client.get('/document/add')
        self.assertEqual(response.status_code, 403)

    def test_add_document_not_authorize_button(self):

        """
        Без специального права не должно быть кнопки на регистрацию документа
        """
        self.client.login(username='test_user1', password='12345')
        response = self.client.get('/')
        response.render()
        self.assertNotIn('/document/add', str(response.content))

    def test_add_document_authorize(self):

        """
        со специальным правом страница должна открываться
        """
        self.client.login(username='test_user2', password='12345')
        response = self.client.get('/document/add')
        self.assertEqual(response.status_code, 200)

    def test_add_document_authorize_button(self):

        """
        Без специального права не должно быть кнопки на регистрацию документа
        """
        self.client.login(username='test_user2', password='12345')
        response = self.client.get('/')
        response.render()
        self.assertIn('/document/add', str(response.content))


    def test_add_document_in_base(self):

        self.counterpart1 = mixer.blend(Counterpart)
        self.classifier1 = mixer.blend(Classifier)
        self.document_type1 = mixer.blend(DocumentType)

        self.client.login(username='test_user2', password='12345')

        doc_before = Document.objects.count()
        response = self.client.post('/document/add',
                                    {'type': self.document_type1.pk,
                                     'nom': '12345', 'date': '01.01.2020',
                                     'counterpart': [self.counterpart1.pk],
                                     'classifier': [self.classifier1.pk],
                                     'description': self.fake.text})
        self.assertEqual(response.status_code, 302)
        doc_after = Document.objects.count()

        self.assertEqual(doc_before+1, doc_after)

    def test_document_pagination(self):

        self.documents = []
        for i in range(0,20):
            self.documents.append(mixer.blend(Document))

        self.client.login(username='test_user1', password='12345')
        response = self.client.get('/p_documents?page=0')
        self.assertEqual(response.status_code, 404)
        response = self.client.get('/p_documents?page=1')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/p_documents?page=2')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/p_documents?page=3')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/p_documents?page=4')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/p_documents?page=5')
        self.assertEqual(response.status_code, 404)