from rest_framework import status,generics,filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated

from account.api.serializers import UserSerializer
from account.models import User

from interview.models import Job,JobApplication,InterviewRound,ApplicationRound,Feedback
from interview.api.serializers import JobSerializer,JobApplicationSerializer,InterviewRoundSerializer,ApplicationRoundSerializer,FeedbackSerializer,JobApplicationStatusUpdateSerializer
from interview.api.permissions import IsAdmin, IsInterviewer, IsCandidate, AdminFullInterviewerReadOnly


class JobListCreateView(generics.ListCreateAPIView):
    '''
    This view is used to create a job and get all jobs
    '''
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AdminFullInterviewerReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'position', 'is_open'] #/jobs/?department=Python
    search_fields = ['title', 'description', 'department'] #/jobs/?search=developer 
    ordering_fields = ['created_at']

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    This view is used to get a job details, update a job and delete a job
    '''
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AdminFullInterviewerReadOnly]

class OpenJobsListView(generics.ListAPIView):
    '''
    This view is used to get all open jobs
    '''
    queryset = Job.objects.filter(is_open = True)
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

class JobApplicationListCreateView(generics.ListCreateAPIView):
    '''
    This view is used to create a job application and get all job applications
    '''
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['status', 'is_selected', 'job']
    ordering_fields = ['applied_on', 'status']
    
    def get_permissions(self):
        if self.request.method == 'POST' and self.request.user.role == 'candidate':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(candidate=self.request.user)

class JobApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    This view is used to get a job application details, update a job application and delete a job application
    '''
    queryset = JobApplication.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH' and 'status' in self.request.data:
            return JobApplicationStatusUpdateSerializer
        return JobApplicationSerializer
    
    def get_permissions(self):
        application = self.get_object()
        if self.request.user.role == 'candidate' and application.candidate == self.request.user and self.request.method in ['GET']:
            self.permission_classes = [IsCandidate]
        else:
            self.permission_classes = [IsAdmin]
        return super().get_permissions()

class JobSpecificApplicationsListView(generics.ListAPIView):
    '''
    This view is used to get all job applications for a specific job
    '''
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        job_id = self.kwargs.get('pk')
        return JobApplication.objects.filter(job_id=job_id)    

class SelectCandidateView(generics.UpdateAPIView):
    '''
    This view is used to select a candidate for a job
    '''
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationStatusUpdateSerializer
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'closed'
        instance.is_selected = True
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MyApplicationsListView(generics.ListAPIView):
    '''
    This view is used to get all job applications for a specific candidate
    '''
    serializer_class = JobApplicationSerializer
    permission_classes = [IsCandidate]
    
    def get_queryset(self):
        user = self.request.user
        if user.role != 'candidate':
            return JobApplication.objects.none()
        return JobApplication.objects.filter(candidate=user)

class InterviewRoundListView(generics.ListCreateAPIView):
    '''
    This view is used to create an interview round and get all interview rounds
    '''
    queryset = InterviewRound.objects.all()
    serializer_class = InterviewRoundSerializer
    permission_classes = [AdminFullInterviewerReadOnly]

class ApplicationRoundListView(generics.ListCreateAPIView):
    '''
    This view is used to create an application round and get all application rounds
    '''
    queryset = ApplicationRound.objects.all()
    serializer_class = ApplicationRoundSerializer
    permission_classes = [AdminFullInterviewerReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['interviewer']
    ordering_fields = ['scheduled_time']

    def get_queryset(self):
        application_id = self.kwargs.get('pk')
        if self.request.user.role == 'admin':
            return ApplicationRound.objects.filter(application_id=application_id)
        elif self.request.user.role == 'interviewer':
            return ApplicationRound.objects.filter(
                application_id=application_id,
                interviewer=self.request.user
            )
        return ApplicationRound.objects.none()

class ApplicationRoundDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    This view is used to get an application round details, update an application round and delete an application round
    '''
    queryset = ApplicationRound.objects.all()
    serializer_class = ApplicationRoundSerializer
    permission_classes = [AdminFullInterviewerReadOnly]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return ApplicationRound.objects.all()
        elif self.request.user.role == 'interviewer':
            return ApplicationRound.objects.filter(interviewer=self.request.user)
        return ApplicationRound.objects.none()

class FeedbackCreateView(generics.CreateAPIView):
    '''
    This view is used to create a feedback
    '''
    serializer_class = FeedbackSerializer
    permission_classes = [IsInterviewer]

    def perform_create(self, serializer):
        user = self.request.user
        application_round = serializer.validated_data['application_round']

        if application_round.interviewer != user and user.role != 'admin':
            return Response(
                {'error': 'You cannot provide feedback for this interview round'},
                status=status.HTTP_403_FORBIDDEN
            )

        feedback = serializer.save(interviewer=user)
         
        # Trigger async task to send notification emails
        from interview.tasks import send_feedback_notification
        send_feedback_notification.delay(feedback.id)

class CandidateFeedbackListView(generics.ListAPIView):
    '''
    This view is used to get all feedbacks for a specific candidate
    '''
    serializer_class = FeedbackSerializer
    permission_classes = [IsCandidate]

    def get_queryset(self):
        user = self.request.user
        
        job_applications = JobApplication.objects.filter(candidate=user)
        application_rounds = ApplicationRound.objects.filter(application__in=job_applications)
        feedbacks = Feedback.objects.filter(application_round__in=application_rounds)
        
        return feedbacks

class MyInterviewsView(generics.ListAPIView):
    '''
    This view is used to get all interviews for a specific interviewer
    '''
    serializer_class = ApplicationRoundSerializer
    permission_classes = [IsInterviewer]

    def get_queryset(self):
        user = self.request.user
        
        if user.role != 'interviewer':
            return ApplicationRound.objects.none()
        
        return ApplicationRound.objects.filter(interviewer=user)

class UpcomingInterviewsView(generics.ListAPIView):
    '''
    This view is used to get all upcoming interviews
    '''
    serializer_class = ApplicationRoundSerializer
    permission_classes = [AdminFullInterviewerReadOnly]
    
    def get_queryset(self):
        from django.utils import timezone
        
        if self.request.user.role == 'admin':
            return ApplicationRound.objects.filter(
                scheduled_time__gt=timezone.now()
            ).order_by('scheduled_time')
        elif self.request.user.role == 'interviewer':
            return ApplicationRound.objects.filter(
                scheduled_time__gt=timezone.now(),
                interviewer=self.request.user
            ).order_by('scheduled_time')
        
        return ApplicationRound.objects.none()


