from rest_framework import status,generics,filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend

from account.api.serializers import UserSerializer
from account.models import User

from interview.models import Job,JobApplication,InterviewRound,ApplicationRound,Feedback
from interview.api.serializers import JobSerializer,JobApplicationSerializer,InterviewRoundSerializer,ApplicationRoundSerializer,FeedbackSerializer,JobApplicationStatusUpdateSerializer


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'position', 'is_open'] #/jobs/?department=Python
    search_fields = ['title', 'description', 'department'] #/jobs/?search=developer 
    ordering_fields = ['created_at']

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobApplicationsListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    
    def get_queryset(self):
        job_id = self.kwargs.get('pk')
        return JobApplication.objects.filter(job_id=job_id) #to get all job applications for a specific job
    
class OpenJobsListView(generics.ListAPIView):
    queryset = Job.objects.filter(is_open = True)
    serializer_class = JobSerializer

class JobApplicationListView(generics.ListCreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['status', 'is_selected', 'job']
    ordering_fields = ['applied_on', 'status']

class JobApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobApplication.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH' and status in self.request.data:
            return JobApplicationStatusUpdateSerializer
        return JobApplicationSerializer

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
    

class MyApplicationsListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role != 'candidate':
            return JobApplication.objects.none()
        return JobApplication.objects.filter(candidate=user)

class InterviewRoundListView(generics.ListCreateAPIView):
    queryset = InterviewRound.objects.all()
    serializer_class = InterviewRoundSerializer

class ApplicationRoundListView(generics.ListCreateAPIView):
    queryset = ApplicationRound.objects.all()
    serializer_class = ApplicationRoundSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['interviewer']
    ordering_fields = ['scheduled_time']

    def get_queryset(self):
        application_id = self.kwargs.get('pk')
        return ApplicationRound.objects.filter(application_id=application_id)

class ApplicationRoundDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationRound.objects.all()
    serializer_class = ApplicationRoundSerializer

class FeedbackCreateView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        user = self.request.user
        application_round = serializer.validated_data['application_round']

        if application_round.interviewer != user and not user.is_staff:
            return Response(
                {'error': 'You cannot provide feedback'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save()

# class CandidateFeedbackListView(generics.ListAPIView):
#     serializer_class = FeedbackSerializer

#     def get_queryset(self):
#         user = self.request.user

#         if user.role != 'candidate':
#             raise PermissionDenied("You are not authorized to view feedbacks.")
        
#         job_applications = JobApplication.objects.filter(candidate=user)
#         application_rounds = ApplicationRound.objects.filter(application__in=job_applications)

#         feedbacks = Feedback.objects.filter(application_round__in=application_rounds)
        
#         return feedbacks

class MyInterviewsView(generics.ListAPIView):
    serializer_class = ApplicationRoundSerializer

    def get_queryset(self):
        user = self.request.user
        
        if user.role != 'interviewer':
            return ApplicationRound.objects.none()
        
        return ApplicationRound.objects.filter(interviewer=user)

class UpcomingInterviewsView(generics.ListAPIView):
    serializer_class = ApplicationRoundSerializer
    
    def get_queryset(self):
        from django.utils import timezone
        
        return ApplicationRound.objects.filter(
            scheduled_time__gt=timezone.now()
        ).order_by('scheduled_time')



