from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from interview.models import Feedback
from account.models import User


@shared_task
def send_feedback_notification(feedback_id):
    """
    This task sends email notifications when feedback is submitted.
    Args:
        feedback_id: The ID of the feedback in the database
    """
    try:

        feedback = Feedback.objects.select_related(
            'application_round__application__candidate',
            'application_round__interviewer',
            'application_round__application__job'
        ).get(id=feedback_id)
        
        # Extract the data for the email
        candidate = feedback.application_round.application.candidate
        interviewer = feedback.application_round.interviewer
        job = feedback.application_round.application.job
        feedback_date = timezone.now().strftime('%Y-%m-%d %H:%M')
        rating = feedback.rating
        comments = feedback.comments  
        
       
        candidate_subject = f"New feedback for your {job.title} application"
        candidate_template_data = {
            'subject': candidate_subject,
            'recipient_name': candidate.first_name,
            'job_title': job.title,
            'interviewer_name': f"{interviewer.first_name} {interviewer.last_name}",
            'feedback_date': feedback_date,
            'comments': comments ,
            'rating': rating
        }
        
     
        candidate_html = render_to_string('emails/feedback_notification.html', candidate_template_data)
        send_feedback_notification_email(candidate.email, candidate_subject, candidate_html)
        
        return f"Notification sent for feedback {feedback_id}"
    
    except Exception as e:
        return f"Error sending notification: {str(e)}"


def send_feedback_notification_email(recipient_email, subject, html_content):
    """
    This function sends the actual email using Django's email system.
    Args:
        recipient_email: The email address to send to
        subject: The email subject line
        html_content: The HTML content of the email (from our template)
    """
    send_mail(
        subject=subject,
        message="This email contains formatted content about interview feedback. Please use an email client that supports HTML to view it properly.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        html_message=html_content,
        fail_silently=False,
    )
    return f"Email sent to {recipient_email}"


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
        interviewer_interviews[interviewer.id]['interviews'].append(interview)
    
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
        IMS Team
   
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[interviewer.email],
            fail_silently=False,
        )

    return f"Sent interview reminders to {len(interviewer_interviews)} interviewers" 