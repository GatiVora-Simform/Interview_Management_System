from django.urls import path
from interview.api.views import (
    JobListCreateView,
    JobDetailView,
    OpenJobsListView,
    JobApplicationListCreateView,
    JobApplicationDetailView,
    JobSpecificApplicationsListView,
    SelectCandidateView,
    MyApplicationsListView,
    InterviewRoundListView,
    ApplicationRoundListView,
    ApplicationRoundDetailView,
    FeedbackCreateView,
    CandidateFeedbackListView,
    MyInterviewsView,
    UpcomingInterviewsView,
)

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('jobs/open/', OpenJobsListView.as_view(), name='open-jobs-list'),
    path('jobs/<int:pk>/applications/', JobSpecificApplicationsListView.as_view(), name='job-applications-list'),
    
    path('applications/', JobApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', JobApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:pk>/select/', SelectCandidateView.as_view(), name='select-candidate'),
    path('applications/me/', MyApplicationsListView.as_view(), name='my-applications'),
    
    path('interview-rounds/', InterviewRoundListView.as_view(), name='interview-round-list'),
    
    path('applications/<int:pk>/rounds/', ApplicationRoundListView.as_view(), name='application-rounds-list'),
    path('application-rounds/<int:pk>/', ApplicationRoundDetailView.as_view(), name='application-round-detail'),
    
    path('application-rounds/<int:pk>/feedback/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('feedback/me/', CandidateFeedbackListView.as_view(), name='my-feedback'),
    
    path('interviews/upcoming/', UpcomingInterviewsView.as_view(), name='upcoming-interviews'),
    path('interviews/me/', MyInterviewsView.as_view(), name='my-interviews'),
]
