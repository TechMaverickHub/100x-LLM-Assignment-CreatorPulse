import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from dotenv import load_dotenv

from app.mail.models import EmailLog
from app.newsletter.models import NewsletterSchedule

logger = logging.getLogger('scheduler')

load_dotenv()


def send_scheduled_newsletters():
    now = timezone.now()
    logger.info(f"Running scheduled newsletter job at {now}")

    print("Hello world", now)
    # Fetch all active schedules due now or earlier
    active_schedules = NewsletterSchedule.objects.filter(
        is_active=True,
        start_time__lte=now
    )

    for schedule in active_schedules:
        draft = schedule.draft
        user = draft.newsletter_template.user

        print(user.email)
        try:
            # Here you can integrate your email sending logic
            # e.g. resend.Emails.send(...)
            print(f"Sent newsletter to {user.email}")

            # Log success
            EmailLog.objects.create(
                user_id=user.pk,
                recipient=user.email,
                message=draft.html_content,
                status='SUCCESS'
            )
        except Exception as e:
            # Log failure
            EmailLog.objects.create(
                user_id=user.pk,
                recipient=user.email,
                message=draft.html_content,
                status='FAILED',
                error_message=str(e)
            )
            logger.error(f"Failed to send newsletter to {user.email}: {e}")

        # Update next run based on frequency
        if schedule.frequency == 'once':
            schedule.is_active = False
        elif schedule.frequency == 'daily':
            schedule.start_time += timezone.timedelta(days=1)
        elif schedule.frequency == 'weekly':
            schedule.start_time += timezone.timedelta(weeks=1)
        elif schedule.frequency == 'monthly':
            schedule.start_time += relativedelta(months=1)

        schedule.save()
        logger.info(f"Updated schedule {schedule.id} for next run: {schedule.start_time}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_scheduled_newsletters,
        trigger=IntervalTrigger(seconds=10),
        name="Send Scheduled Newsletters",
        replace_existing=True
    )
    scheduler.start()
    logger.info("Newsletter scheduler started (runs every 10 minutes)")
