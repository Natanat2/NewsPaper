# signals.py
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .tasks import process_post_category_changed
from .models import Post

@receiver(m2m_changed, sender=Post.postCategory.through)
def post_category_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        process_post_category_changed.delay(instance.id)
