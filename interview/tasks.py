from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta

@shared_task
def send_feedback_notification(feedback_id):

    from interview.models import Feedback
    from account.models import User
    
    try:
        feedback = Feedback.objects.select_related(
            'application_round__application__candidate',
            'application_round__interviewer'
        ).get(id=feedback_id)
        
        candidate = feedback.application_round.application.candidate
        interviewer = feedback.application_round.interviewer
        job_title = feedback.application_round.application.job.title
        
        candidate_subject = f"New feedback for your {job_title} application"
        candidate_message = f"""
        Hello {candidate.first_name},
        
        A new feedback has been submitted for your application to {job_title}.
        
        Interviewer: {interviewer.first_name} {interviewer.last_name}
        Date: {timezone.now().strftime('%Y-%m-%d %H:%M')}
        
        You can check your feedback in your application dashboard.
        
        Best regards,
        IMS Team
        """
        
        send_mail(
            subject=candidate_subject,
            message=candidate_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[candidate.email],
            fail_silently=False,
        )
        
        
        return f"Notification sent for feedback {feedback_id}"
    
    except Feedback.DoesNotExist:
        return f"Feedback with ID {feedback_id} not found"
    except Exception as e:
        return f"Error sending notification: {str(e)}"