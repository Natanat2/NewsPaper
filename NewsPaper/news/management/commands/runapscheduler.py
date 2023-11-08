from datetime import datetime, timedelta
from django.utils import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from news.models import Post, Category, Subscriber
from django.core.mail import EmailMultiAlternatives

def send_weekly_article_list():
    # Получите текущую дату
    current_date = datetime.now()

    # Найдите последнюю дату отправки для задачи
    last_execution = DjangoJobExecution.objects.filter(job__id='send_weekly_article_list').last()

    # Если последняя дата выполнения существует, используйте ее
    if last_execution:
        last_execution_date = last_execution.run_etime.astimezone(timezone(settings.TIME_ZONE))
    else:
        last_execution_date = current_date - timedelta(weeks=1)

    # Найдите все статьи, которые были опубликованы после последней отправки
    new_articles = Post.objects.filter(dateCreation__gt=last_execution_date)

    # Сгруппируйте статьи по категориям
    articles_by_category = {}
    for article in new_articles:
        for category in article.postCategory.all():
            articles_by_category.setdefault(category, []).append(article)

    # Отправьте список статей подписчикам категорий
    for category, articles in articles_by_category.items():
        subscribers = Subscriber.objects.filter(category=category)
        if subscribers:
            subject = f'Новые статьи в категории {category.name}'
            text_content = 'Новые статьи:\n\n'
            for article in articles:
                text_content += f'{article.title}\n{article.get_absolute_url()}\n\n'

            for subscriber in subscribers:
                msg = EmailMultiAlternatives(subject, text_content, None, [subscriber.user.email])
                msg.send()

    # Обновите последнюю дату выполнения задачи
    if last_execution:
        last_execution.run_etime = current_date
        last_execution.save()
    else:
        DjangoJobExecution(job_id='send_weekly_article_list', run_etime=current_date).save()

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_article_list,
            trigger=CronTrigger(day_of_week="mon", hour="8"),
            id="send_weekly_article_list",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'send_weekly_article_list'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
