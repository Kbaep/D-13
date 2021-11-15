from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail
from .models import Post, Subscriber
from datetime import datetime, timedelta
from django.template.loader import render_to_string


@receiver(pre_save, sender=Post)
def check_max_post_today(sender, instance, **kwargs):
    date_from = datetime.now() - timedelta(days=1)
    post_count_today = len(Post.objects.filter(author=instance.author, created__gte=date_from))

    if post_count_today >= 3:
        raise Exception('More than 3 post today created')

def notify_subs(sender, instance, created, **kwargs):
    if created:
        post = instance
        for category in post.created_category_list:
            post.category.add(category)
        categories = post.category.all()
        for category in categories:
            subs = Subscriber.objects.filter(category=category)
            for sub in subs:
                html_content = render_to_string(
                    'mail/category_post.html',
                    {
                        'sub': sub,
                        'post': post,
                        "category": category
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f"New Post in {category.title}! {post.title}",
                    body=post.text[:50],
                    from_email='kryglov.d@yandex.ru',
                    to=[sub.user.email]
                )
                msg.attach_alternative(html_content, "text/html")

                msg.send()