from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post,Category, Subscriber


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    post_categories = instance.postCategory.all()

    subscribers = User.objects.filter(subscriptions__category__in=post_categories)

    emails = User.objects.filter(
        Subscriber__category=instance.category
    ).values_list('email', flat=True)

    subject = f'Вышла новая новость в категории {instance.category}'

    text_content = (
        f'Товар: {instance.name}\n'
        f'Цена: {instance.price}\n\n'
        f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Товар: {instance.name}<br>'
        f'Цена: {instance.price}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Ссылка на новость:</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
