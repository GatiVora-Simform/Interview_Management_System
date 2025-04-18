from rest_framework.test import APITestCase
from interview.models import Job
from account.models import User
from django.urls import reverse
from rest_framework import status

class JobAPITestCase(APITestCase):
    
    def setUp(self):
        self.admin_user = User.objects.create_user(
            email="admin.test@example.com",
            password="admin",
            first_name="Admin",
            last_name="User",
            role="admin",
        )

        self.interviewer_user = User.objects.create_user(
            email="interviewer.test@example.com",
            password="interviewer",
            first_name="Interviewer",
            last_name="User",
            role="interviewer",
        )
        
        self.candidate_user = User.objects.create_user(
            email="candidate@example.com",
            password="password123",
            first_name="Candidate",
            last_name="User",
            role="candidate"
        )

        self.job1 = Job.objects.create(
            title="Python Developer",
            description="We need a Python developer",
            department="Engineering",
            position="software_engineer",
            is_open=True
        )

        self.job_list_create_url = reverse('job-list-create')
        self.job_detail_url = reverse('job-detail', kwargs={'pk': self.job1.id})
        self.open_job_url = reverse('open-jobs-list')

    def test_create_job_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "title": "Frontend Developer",
            "description": "We need a Frontend developer",
            "department": "Engineering",
            "position": "software_engineer",
            "is_open": True
        }
        response = self.client.post(self.job_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 2)

    def test_create_job_as_candidate(self):
        self.client.force_authenticate(user=self.candidate_user)
        data = {
            "title": "Frontend Developer",
            "description": "We need a Frontend developer",
            "department": "Engineering",
            "position": "software_engineer",
            "is_open": True
        }
        response = self.client.post(self.job_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_jobs_as_admin(self):

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.job_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_jobs_as_candidate(self):

        self.client.force_authenticate(user=self.candidate_user)
        response = self.client.get(self.job_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_open_jobs(self):

        self.client.force_authenticate(user = self.admin_user)
        response = self.client.get(self.open_job_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_job_detail(self):
        self.client.force_authenticate(user = self.admin_user)
        response = self.client.get(self.job_detail_url,kwargs={'pk':self.job1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'],self.job1.title)
        self.assertEqual(response.data['description'],self.job1.description)
        self.assertEqual(response.data['department'],self.job1.department)
