# tasks.py
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from .models import Post

@shared_task
def process_post_category_changed(post_id):
    instance = Post.objects.get(pk=post_id)
    category_names = instance.postCategory.all().values_list('name', flat=True)
    category_names_str = ', '.join(category_names)
    subscribers = User.objects.filter(subscriptions__category__in=instance.postCategory.all()).distinct()

    subject = f'Вышла новая новость в категории {category_names_str}'
    text_content = (
        f'Заголовок: {instance.title}\n'
        f'Текст: {instance.text}\n\n'
        f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )

    for subscriber in subscribers:
        msg = EmailMultiAlternatives(subject, text_content, None, [subscriber.email])
        msg.send()
