from rest_framework import status,generics,filters
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.api.serializers import UserSerializer
from account.models import User

from interview.models import Job,JobApplication,InterviewRound,ApplicationRound,Feedback
from interview.api.serializers import JobSerializer,JobApplicationSerializer,InterviewRoundSerializer,ApplicationRoundSerializer,FeedbackSerializer,JobApplicationStatusUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend

class JobListCreateView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'position', 'is_open'] #/jobs/?department=Python
    search_fields = ['title', 'description', 'department'] #/jobs/?search=developer 
    ordering_fields = ['created_at']

class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobApplicationsList(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    
    def get_queryset(self):
        job_id = self.kwargs.get('pk')
        return JobApplication.objects.filter(job_id=job_id) #to get all job applications for a specific job
    
class JobApplicationList(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['status', 'is_selected', 'job']
    ordering_fields = ['applied_on', 'status']

class JobApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobApplication.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH' and status in self.request.data:
            return JobApplicationStatusUpdateSerializer
        return JobApplicationSerializer

class InterviewRoundList(generics.ListCreateAPIView):
    queryset = InterviewRound.objects.all()
    serializer_class = InterviewRoundSerializer

class InterviewRoundDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InterviewRound.objects.all()
    serializer_class = InterviewRoundSerializer

class ApplicationRoundList(generics.ListCreateAPIView):
    queryset = ApplicationRound.objects.all()
    serializer_class = ApplicationRoundSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['interviewer']
    ordering_fields = ['scheduled_time']

    def get_queryset(self):
        application_id = self.kwargs.get('pk')
        return ApplicationRound.objects.filter(application_id=application_id)

class ApplicationRoundDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationRound.objects.all()
    serializer_class = ApplicationRoundSerializer


class MyApplications(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role != 'candidate':
            return JobApplication.objects.none()
        
        return JobApplication.objects.filter(candidate=user)


class MyInterviews(generics.ListAPIView):
    serializer_class = ApplicationRoundSerializer

    def get_queryset(self):
        user = self.request.user
        
        if user.role != 'interviewer':
            return ApplicationRound.objects.none()
        
        return ApplicationRound.objects.filter(interviewer=user)

class UpcomingInterviews(generics.ListAPIView):
    serializer_class = ApplicationRoundSerializer
    
    def get_queryset(self):
        from django.utils import timezone
        
        return ApplicationRound.objects.filter(
            scheduled_time__gt=timezone.now()
        ).order_by('scheduled_time')


class SelectCandidateView(generics.UpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationStatusUpdateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'closed'
        instance.is_selected = True
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
##feedback left

