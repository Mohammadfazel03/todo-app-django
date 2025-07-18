from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from task.models import Task

User = get_user_model()


class TestTaskAPI(TestCase):
    def setUp(self):
        self.active_user = User.objects.create_user(
            email='active@test.com',
            password='jenfbfuyhebfnei',
            is_active=True
        )
        self.active_user2 = User.objects.create_user(
            email='active2@test.com',
            password='jenfbfuyhebfnei',
            is_active=True
        )
        self.task = Task.objects.create(
            content='test',
            is_complete=False,
            user=self.active_user,
        )
        self.task2 = Task.objects.create(
            content='test',
            is_complete=False,
            user=self.active_user2,
        )
        user_2_tasks = [Task(content=f'user_2_task_{i}', is_complete=i % 2, user=self.active_user2) for i in range(6)]
        user_1_tasks = [Task(content=f'user_1_task_{i}', is_complete=i % 2, user=self.active_user) for i in range(10)]
        Task.objects.bulk_create(user_1_tasks)
        Task.objects.bulk_create(user_2_tasks)
        self.client = APIClient()

    def test_create_task_successfully(self):
        credentials_data = {
            "email": 'active@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        data = {
            'content': "ieuniufn",
            'is_complete': True
        }
        response = self.client.post('/api/v1/task/', data=data, headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 201)
        json_res = response.json()
        self.assertTrue('id' in json_res)
        self.assertTrue('content' in json_res)
        self.assertTrue('is_complete' in json_res)
        self.assertTrue('created_at' in json_res)
        self.assertTrue('updated_at' in json_res)
        obj = Task.objects.get(id=json_res['id'])
        self.assertFalse(obj.is_complete)

    def test_create_task_unauthorized(self):
        data = {
            'content': "ieuniufn"
        }
        before_request_task_count = Task.objects.count()
        response = self.client.post('/api/v1/task/', data=data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Task.objects.count(), before_request_task_count)

    def test_create_task_bad_request(self):
        credentials_data = {
            "email": 'active@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        data = {
            'is_complete': True
        }
        before_request_task_count = Task.objects.count()
        response = self.client.post('/api/v1/task/', data=data, headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Task.objects.count(), before_request_task_count)

    def test_edit_task_successfully(self):
        credentials_data = {
            "email": 'active@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        data = {
            'content': "edited test",
            'is_complete': True
        }
        response = self.client.put(f'/api/v1/task/{self.task.pk}/', data=data,
                                   headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 200)
        obj = Task.objects.get(pk=self.task.pk)
        self.assertEqual(obj.content, data['content'])
        self.assertEqual(obj.is_complete, False)

    def test_edit_task_wrong_user(self):
        credentials_data = {
            "email": 'active2@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        data = {
            'content': "edited test"
        }
        response = self.client.put(f'/api/v1/task/{self.task.pk}/', data=data,
                                   headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 404)
        obj = Task.objects.get(pk=self.task.pk)
        self.assertEqual(obj, self.task)

    def test_edit_task_unauthenticated_user(self):
        data = {
            'content': "edited test"
        }
        response = self.client.put(f'/api/v1/task/{self.task.pk}/', data=data)
        self.assertEqual(response.status_code, 401)
        obj = Task.objects.get(pk=self.task.pk)
        self.assertEqual(obj, self.task)

    def test_delete_task_successfully(self):
        credentials_data = {
            "email": 'active@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        response = self.client.delete(f'/api/v1/task/{self.task.pk}/',
                                      headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task.pk)

    def test_delete_task_wrong_user(self):
        credentials_data = {
            "email": 'active2@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        response = self.client.delete(f'/api/v1/task/{self.task.pk}/',
                                      headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 404)
        Task.objects.get(pk=self.task.pk)

    def test_delete_task_unauthenticated_user(self):
        response = self.client.delete(f'/api/v1/task/{self.task.pk}/')
        self.assertEqual(response.status_code, 401)
        Task.objects.get(pk=self.task.pk)

    def test_get_task_successfully(self):
        credentials_data = {
            "email": 'active@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        response = self.client.get(f'/api/v1/task/{self.task.pk}/', headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 200)
        json_res = response.json()
        self.assertTrue('id' in json_res)
        self.assertTrue('content' in json_res)
        self.assertTrue('is_complete' in json_res)
        self.assertTrue('created_at' in json_res)
        self.assertTrue('updated_at' in json_res)

    def test_get_task_wrong_user(self):
        credentials_data = {
            "email": 'active@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        response = self.client.get(f'/api/v1/task/{self.task2.pk}/', headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 404)

    def test_get_task_unauthenticated_user(self):
        response = self.client.get(f'/api/v1/task/{self.task2.pk}/')
        self.assertEqual(response.status_code, 401)

    def test_list_tasks_successfully(self):
        credentials_data = {
            "email": 'active@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        response = self.client.get('/api/v1/task/', headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 200)
        json_res = response.json()
        self.assertEqual(len(json_res), Task.objects.filter(user=self.active_user).count())

    def test_list_task_unauthenticated_user(self):
        response = self.client.get('/api/v1/task/')
        self.assertEqual(response.status_code, 401)

    def test_change_state_task_successfully(self):
        credentials_data = {
            "email": 'active@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        data = {
            'content': "edited test",
            'is_complete': True
        }
        response = self.client.post(f'/api/v1/task/change_state/{self.task.pk}/', data=data,
                                    headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 200)
        obj = Task.objects.get(pk=self.task.pk)
        self.assertEqual(obj.content, self.task.content)
        self.assertEqual(obj.is_complete, data['is_complete'])

    def test_change_state_task_wrong_user(self):
        credentials_data = {
            "email": 'active2@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        data = {
            'is_complete': True
        }
        response = self.client.post(f'/api/v1/task/change_state/{self.task.pk}/', data=data,
                                    headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 403)
        obj = Task.objects.get(pk=self.task.pk)
        self.assertEqual(obj, self.task)

    def test_change_state_task_bad_request(self):
        credentials_data = {
            "email": 'active@test.com',
            "password": 'jenfbfuyhebfnei',
        }
        credentials_response = self.client.post('/api/v1/jwt/login/', data=credentials_data)
        access = credentials_response.json()['access']
        data = {
            'is_complete': "wrong"
        }
        response = self.client.post(f'/api/v1/task/change_state/{self.task.pk}/', data=data,
                                    headers={'Authorization': 'Bearer ' + access})
        self.assertEqual(response.status_code, 400)
        obj = Task.objects.get(pk=self.task.pk)
        self.assertEqual(obj, self.task)

    def test_change_state_task_unauthenticated_user(self):
        data = {
            'is_complete': True
        }
        response = self.client.put(f'/api/v1/task/change_state/{self.task.pk}/', data=data)
        self.assertEqual(response.status_code, 401)
        obj = Task.objects.get(pk=self.task.pk)
        self.assertEqual(obj, self.task)
