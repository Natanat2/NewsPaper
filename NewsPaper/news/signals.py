from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post


@receiver(m2m_changed, sender = Post.postCategory.through)
def post_category_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":

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
