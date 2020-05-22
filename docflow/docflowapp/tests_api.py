from django.test import Client
from rest_framework.test import APIClient
from django.test import TestCase
from usersapp.models import DocFlowUser


class APITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = DocFlowUser.objects.create_user(username='test_user1', email='test1@test.com', password='12345',
                                                     can_add_documents=False, can_find_documents=False)
        self.user2 = DocFlowUser.objects.create_user(username='test_user2', email='test1@test.com', password='12345',
                                                     can_add_documents=True, can_find_documents=False)
        self.user3 = DocFlowUser.objects.create_user(username='test_user3', email='test1@test.com', password='12345',
                                                     can_add_documents=False, can_find_documents=True)
        self.user4 = DocFlowUser.objects.create_user(username='test_user4', email='test1@test.com', password='12345',
                                                     can_add_documents=True, can_find_documents=True)

    def test_api_login_required(self):

        """
        Должен при неавторизованном входе возвращаеть 403
        """
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 403)


    def test_api_login(self):

        """
        При логине заходим на страницу
        """
        self.client.login(username='test_user1', password='12345')
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)