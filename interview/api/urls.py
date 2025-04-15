from django.urls import path
from interview.api.views import (JobListCreateView,JobDetailView,JobApplicationsListView,OpenJobsListView,JobApplicationListView,
                                 JobApplicationDetailView,SelectCandidateView,MyApplicationsListView,InterviewRoundListView,
                                 ApplicationRoundListView,FeedbackCreateView,UpcomingInterviewsView,CandidateFeedbackListView)

urlpatterns = [
    path('job/',JobListCreateView.as_view(),name='job-list-create'),
    path('job/<int:pk>/',JobDetailView.as_view(),name='job-detail'),

    path('job/open/',OpenJobsListView.as_view(),name='open-jobs'),

    path('job/application/',JobApplicationListView.as_view(),name='create-application'),
    path('job/<int:pk>/applications/',JobApplicationsListView.as_view(),name='job-applications'),
    path('applications/',JobApplicationsListView.as_view(),name='applications-list'),
    path('applications/<int:pk>',JobApplicationDetailView.as_view(),name='application-detail'),
    path('applications/<int:pk>/select/',SelectCandidateView.as_view(),name='select-candidate'),
    path('my-applications/',MyApplicationsListView.as_view(),name='my-applications'),

    path('interview-rounds/',InterviewRoundListView.as_view(),name='rounds-list'),

    path('application/<int:pk>/round/',ApplicationRoundListView.as_view(),name='application-round-detail'),
    path('application-round/<int:pk>/feedback/',FeedbackCreateView.as_view(),name='create-feedback'),
    
    path('upcoming-interviews/',UpcomingInterviewsView.as_view(), name='upcoming-interviews'),

    path('feedback/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('my-feedback/',CandidateFeedbackListView.as_view(), name='my-feedback')
]



# from django.urls import path
# from . import views

# urlpatterns = [
#     # Job-related URLs
#     path('jobs/', views.JobListCreateView.as_view(), name='job-list-create'),
#     path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    
#     # Job Application-related URLs
#     path('jobs/<int:pk>/applications/', views.JobApplicationsListView.as_view(), name='job-applications-list'),
#     path('applications/', views.JobApplicationListView.as_view(), name='job-application-list'),
#     path('applications/<int:pk>/', views.JobApplicationDetailView.as_view(), name='job-application-detail'),
#     path('applications/select/<int:pk>/', views.SelectCandidateView.as_view(), name='select-candidate'),
#     path('my-applications/', views.MyApplicationsListView.as_view(), name='my-applications'),

#     # Interview Round-related URLs
#     path('interview-rounds/', views.InterviewRoundListView.as_view(), name='interview-round-list'),

#     # Application Round-related URLs
#     path('application-rounds/', views.ApplicationRoundListView.as_view(), name='application-round-list'),
#     path('application-rounds/<int:pk>/', views.ApplicationRoundDetailView.as_view(), name='application-round-detail'),
    
#     # Feedback-related URLs
#     path('feedback/', views.FeedbackCreateView.as_view(), name='feedback-create'),
#     path('my-feedback/', views.CandidateFeedbackListView.as_view(), name='my-feedback'),
    
#     # Interview-related URLs
#     path('my-interviews/', views.MyInterviewsView.as_view(), name='my-interviews'),
#     path('upcoming-interviews/', views.UpcomingInterviewsView.as_view(), name='upcoming-interviews'),
#     path('open-jobs/', views.OpenJobsListView.as_view(), name='open-jobs-list'),
# ]
