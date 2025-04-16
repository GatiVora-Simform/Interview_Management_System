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
    

@shared_task
def send_interview_reminders():

    from interview.models import ApplicationRound
    
    now = timezone.now()  
    next_24_hours = now + timedelta(hours=24)  
    
    upcoming_interviews = ApplicationRound.objects.filter(
        scheduled_time__gt=now,  
        scheduled_time__lte=next_24_hours 
    ).select_related(
        'interviewer',
        'application__candidate',
        'application__job'
    )
    
    # Group interviews by interviewer
    interviewer_interviews = {}
    for interview in upcoming_interviews:
        interviewer = interview.interviewer
        # If this is the first interview for this interviewer, create an entry
        if interviewer.id not in interviewer_interviews:
            interviewer_interviews[interviewer.id] = {
                'interviewer': interviewer,
                'interviews': []
            }
        # Add this interview to the interviewer's list
        interviewer_interviews[interviewer.id]['interviews'].append(interview)
    
    # Send reminder emails to each interviewer
    for interviewer_data in interviewer_interviews.values():
        interviewer = interviewer_data['interviewer']
        interviews = interviewer_data['interviews']
        
        subject = f"Reminder: You have {len(interviews)} interview(s) scheduled in the next 24 hours"
        
        message = f"""
        Hello {interviewer.first_name},
        
        This is a reminder that you have the following interview(s) scheduled in the next 24 hours:
        
        """
        
        # Add details for each interview
        for interview in interviews:
            candidate = interview.application.candidate
            job = interview.application.job
            interview_time = interview.scheduled_time
            formatted_time = interview_time.strftime('%Y-%m-%d %H:%M')
            
            # Add this interview to the message
            message += f"""
                * {formatted_time} - {job.title}
                Candidate: {candidate.first_name} {candidate.last_name}
                Email: {candidate.email}
                Phone: {candidate.phone}
            """
        
        message += f"""
        
        Please be prepared and on time for your interviews.
        
        Best regards,
   
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[interviewer.email],
            fail_silently=False,
        )

    return f"Sent interview reminders to {len(interviewer_interviews)} interviewers" 