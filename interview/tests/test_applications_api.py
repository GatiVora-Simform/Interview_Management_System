from rest_framework.test import APITestCase
from interview.models import Job, JobApplication
from account.models import User
from django.urls import reverse
from rest_framework import status

class ApplicationAPITestCase(APITestCase):

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
        self.candidate_user2 = User.objects.create_user(
            email="candidate2@example.com",
            password="password123",
            first_name="Candidate2",
            last_name="User",
            role="candidate"
        )

        self.job = Job.objects.create(
            title="Python Developer",
            description="We need a Python developer",
            department="Engineering",
            position="software_engineer",
            is_open=True
        )

        self.job_application = JobApplication.objects.create(
            job=self.job,
            candidate=self.candidate_user,
            status="new",
            is_selected=False
        )

        self.application_list_create_url = reverse('application-list-create')
        self.application_detail_url = reverse('application-detail', kwargs={'pk': self.job_application.id})
        self.my_applications_url = reverse('my-applications')

    def test_application_create(self):
        self.client.force_authenticate(user=self.candidate_user)
        
        data = {
            "job": self.job.id,
            "candidate": self.candidate_user2.id
        }

        response = self.client.post(self.application_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.count(), 2)

    def test_applications_list(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.application_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_my_applications(self):
        self.client.force_authenticate(user=self.candidate_user)
        response = self.client.get(self.my_applications_url)

        print("response", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


