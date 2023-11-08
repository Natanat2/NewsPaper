# tasks.py
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from .models import Post

from datetime import datetime, timedelta
from django.utils import timezone
from news.models import Post, Category, Subscriber
from django.core.mail import EmailMultiAlternatives


@shared_task()
def send_weekly_article_list():
    # Получите текущую дату
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


@shared_task
def process_post_category_changed(post_id):
    instance = Post.objects.get(pk = post_id)
    category_names = instance.postCategory.all().values_list('name', flat = True)
    category_names_str = ', '.join(category_names)
    subscribers = User.objects.filter(subscriptions__category__in = instance.postCategory.all()).distinct()

    subject = f'Вышла новая новость в категории {category_names_str}'
    text_content = (
        f'Заголовок: {instance.title}\n'
        f'Текст: {instance.text}\n\n'
        f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(subject, text_content, None, [subscriber.email])
        msg.send()
