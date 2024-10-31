from copy import deepcopy

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from apps.user_api.constants import PHONE_NUMBER_VALIDATION_ERROR_MESSAGE
from apps.user_api.models import get_storage, User
from apps.user_api.serializers import UserSerializer
from apps.user_api.utils import remove_test_uploads_folder


class FileCleanUpTestCase(TestCase):
    def setUp(self) -> None:
        self.upload_storage_path = get_storage().location
        super().setUp()

    def tearDown(self) -> None:
        remove_test_uploads_folder(self.upload_storage_path)
        super().tearDown()


class UserTestCase(FileCleanUpTestCase):
    def setUp(self) -> None:
        # TODO: use a factory for those test data values
        self.test_data = {'username': 'test', 'phone_number': '1234567890', 'email': 'test@test.com'}
        self.test_data_1 = {'username': 'test1', 'phone_number': '1234567891', 'email': 'test@test.com'}
        self.test_data_2 = {'username': 'test2', 'phone_number': '1234567899', 'email': 'test1@test.com'}
        self.test_user = User.objects.create(**self.test_data)
        self.user_list_url = reverse('user-list')
        self.user_detail_url = reverse('user-detail', kwargs={'pk': self.test_user.id})
        super().setUp()

    def test_list_users(self):
        resp = self.client.get(self.user_list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp_json = resp.json()
        self.assertEqual(resp_json['count'], 1)
        self.assertIsNone(resp_json['next'])
        self.assertEqual(len(resp_json['results']), 1)
        self.assertEqual([UserSerializer(self.test_user).data], resp_json['results'])

    def test_create_user(self):
        resp = self.client.post(self.user_list_url, data=self.test_data_1)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        resp_dict = resp.json()
        self.assertTrue(self.test_data_1.items() <= resp_dict.items())
        created_user_id = resp_dict['id']
        created_user_object = User.objects.get(id=created_user_id)
        self.assertEqual(UserSerializer(created_user_object).data, resp_dict)

    def test_user_detail(self):
        resp = self.client.get(self.user_detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp_dict = resp.json()
        self.assertEqual(UserSerializer(self.test_user).data, resp_dict)

    def test_user_update(self):
        resp = self.client.patch(
            self.user_detail_url,
            data=self.test_data_2,
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(self.test_data_2.items() <= resp.json().items())
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.username, self.test_data_2['username'])
        self.assertEqual(self.test_user.email, self.test_data_2['email'])
        self.assertEqual(self.test_user.phone_number, self.test_data_2['phone_number'])

    def test_user_delete(self):
        resp = self.client.delete(self.user_detail_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            _ = User.objects.get(id=self.test_user.id)

    def test_create_user_required_fields(self):
        resp = self.client.post(self.user_list_url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json(),
            {x: ['This field is required.'] for x in self.test_data.keys()}
        )
        resp = self.client.post(
            self.user_list_url,
            data={x: '' for x in self.test_data_1.keys()}
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json(),
            {x: ['This field may not be blank.'] for x in self.test_data.keys()}
        )

    def test_create_user_phone_number_validation(self):
        data = deepcopy(self.test_data_1)
        data['phone_number'] = '123'
        resp = self.client.post(self.user_list_url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json(),
            {'phone_number': [PHONE_NUMBER_VALIDATION_ERROR_MESSAGE]}
        )

    def test_create_user_email_validation(self):
        data = deepcopy(self.test_data_1)
        data['email'] = 'test'
        resp = self.client.post(self.user_list_url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json(),
            {'email': ['Enter a valid email address.']}
        )

    def test_create_username_validation(self):
        data = deepcopy(self.test_data_1)
        data['username'] = '#'
        resp = self.client.post(self.user_list_url, data=data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            resp.json(),
            {
                'username': [
                    'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'
                ]
            }
        )
