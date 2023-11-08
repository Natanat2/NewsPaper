from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from news.models import Post, Category, Subscriber
from django.core.mail import EmailMultiAlternatives

from NewsPaper.celery import app
from celery.schedules import crontab

@app.task
def weekly_send_mon_8():

    current_date = datetime.now()

    # Найдите последнюю дату отправки для задачи
    last_execution = DjangoJobExecution.objects.filter(job__id = 'send_weekly_article_list').last()

    # Если последняя дата выполнения существует, используйте ее
    if last_execution:
        last_execution_date = last_execution.run_etime.astimezone(timezone(settings.TIME_ZONE))
    else:
        last_execution_date = current_date - timedelta(weeks = 1)

    # Найдите все статьи, которые были опубликованы после последней отправки
    new_articles = Post.objects.filter(dateCreation__gt = last_execution_date)

    # Сгруппируйте статьи по категориям
    articles_by_category = {}
    for article in new_articles:
        for category in article.postCategory.all():
            articles_by_category.setdefault(category, []).append(article)

    # Отправьте список статей подписчикам категорий
    for category, articles in articles_by_category.items():
        subscribers = Subscriber.objects.filter(category = category)
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
        DjangoJobExecution(job_id = 'send_weekly_article_list', run_etime = current_date).save()
    print('Рассылка отправлена')


app.conf.beat_schedule = {
    'send-weekly-articles': {
        'task': 'tasks.weekly_send_mon_8',
        'schedule': crontab(hour=8, minute=0, day_of_week='mon'),
    },
}

