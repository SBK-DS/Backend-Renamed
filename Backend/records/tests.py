# records/tests.py
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from records.models import BasicDetailsM, DailyRecordsNameM, DailyRecordsValueM


class BasicDetailsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_basic_details(self):
        url = '/besicdetails/'
        data = {
            "user": self.user.id,
            "date_of_diagnosis": "2023-01-01T00:00:00Z",
            "admitted_in_hospital": "2023-01-01T00:00:00Z",
            "covid_test_done": "Yes",
            "covid_test_type": "PCR",
            "covid_test_report": "Negative"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BasicDetailsM.objects.count(), 1)
        self.assertEqual(BasicDetailsM.objects.get().covid_test_done, 'Yes')

    def test_get_basic_details(self):
        BasicDetailsM.objects.create(user=self.user, covid_test_done='Yes', covid_test_type='PCR', covid_test_report='Negative')
        url = f'/besicdetails/{self.user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['covid_test_done'], 'Yes')

    def test_update_basic_details(self):
        basic_details = BasicDetailsM.objects.create(user=self.user, covid_test_done='Yes', covid_test_type='PCR', covid_test_report='Negative')
        url = f'/besicdetails/{self.user.id}/'
        data = {
            "user": self.user.id,
            "covid_test_done": "No",
            "covid_test_type": "Antigen",
            "covid_test_report": "Positive"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        basic_details.refresh_from_db()
        self.assertEqual(basic_details.covid_test_done, 'No')

    def test_delete_basic_details(self):
        basic_details = BasicDetailsM.objects.create(user=self.user, covid_test_done='Yes', covid_test_type='PCR', covid_test_report='Negative')
        url = f'/besicdetails/{self.user.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BasicDetailsM.objects.count(), 0)


class DailyRecordsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.record_name = DailyRecordsNameM.objects.create(recordname="Temperature")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_daily_record(self):
        url = '/dailyrecords/'
        data = {
            "user": self.user.id,
            "recordname": self.record_name.id,
            "value": 98,
            "datetime": "2023-01-01T00:00:00Z"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DailyRecordsValueM.objects.count(), 1)
        self.assertEqual(DailyRecordsValueM.objects.get().value, 98)

    def test_get_daily_records(self):
        DailyRecordsValueM.objects.create(user=self.user, recordname=self.record_name, value=98)
        url = f'/dailyrecords/{self.user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['value'], 98)

    def test_update_daily_record(self):
        daily_record = DailyRecordsValueM.objects.create(user=self.user, recordname=self.record_name, value=98)
        url = f'/dailyrecords/{daily_record.id}/'
        data = {
            "user": self.user.id,
            "recordname": self.record_name.id,
            "value": 99,
            "datetime": "2023-01-01T00:00:00Z"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        daily_record.refresh_from_db()
        self.assertEqual(daily_record.value, 99)

    def test_delete_daily_record(self):
        daily_record = DailyRecordsValueM.objects.create(user=self.user, recordname=self.record_name, value=98)
        url = f'/dailyrecords/{self.user.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DailyRecordsValueM.objects.count(), 0)
