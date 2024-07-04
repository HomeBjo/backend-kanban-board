from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from tasks.models import Task, Subtask


class TaskTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.task = Task.objects.create(title='Test Task', description='Test Description', author=self.user)

    def test_get_all_tasks(self):
        response = self.client.get('/task/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        
    def test_create_task(self):
        data = {'title': 'New Task', 'description': 'New Description'}
        response = self.client.post('/task/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'New Task')
        
    def test_update_task(self):
        data = {'title': 'Updated Task'}
        response = self.client.patch(f'/task/{self.task.pk}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Task')
        
    def test_delete_task(self):
        response = self.client.delete(f'/task/{self.task.pk}/')
        self.assertEqual(response.status_code, 204)
        
  
    def test_delete_subtask(self):
        subtask = Subtask.objects.create(value='Test Subtask', status=False, task=self.task)
        response = self.client.delete(f'/task/{self.task.pk}/subtasks/{subtask.pk}/')
        print("Response Status Code (Delete):", response.status_code)  # Debugging-Statement
        self.assertEqual(response.status_code, 204)
        
    def test_create_subtask(self):
        data = {'value': 'New Subtask', 'status': False}
        response = self.client.post(f'/task/{self.task.pk}/subtasks/', data, format='json')
        print("Response Data (Create):", response.data)  # Debugging-Statement
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['value'], 'New Subtask')
        
    # def test_update_subtask(self):
    #     subtask = Subtask.objects.create(value='Test Subtask', status=False, task=self.task)
    #     data = {'value': 'Updated Subtask'}
    #     response = self.client.patch(f'/task/{self.task.pk}/subtasks/{subtask.pk}/', data, format='json')
    #     print("Response Data (Update):", response.data)  # Debugging-Statement
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data['value'], 'Updated Subtask')

  
