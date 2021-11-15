from celery import shared_task
from datetime import datetime, timezone, timedelta

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from .models import Category, Post


@shared_task
def send_to_subscribers():
    """ Рассылает пользователям список статей из тех категорий, на которые они подписаны, за неделю """
    categories = Category.objects.all()
    for category in categories:
        cat_posts = category.post_set.filter(creation_datetime__gt=datetime.now(timezone.utc) - timedelta(days=7))
        print(category, cat_posts)
        if cat_posts:
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                print(subscriber)
                if subscriber.email:
                    print('отправка...')
                    # Отправка HTML
                    html_content = render_to_string(
                        'mail_week.html', {
                            'category': category,
                            'cat_posts': cat_posts,
                        }
                    )
                    msg = EmailMultiAlternatives(
                        subject='Список новостей за неделю',
                        from_email='kryglov.d@yandex.ru',
                        to=[subscriber.email, ],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()


@shared_task
def notify_subscribers(post_pk):
    """ Отправляет по почте информацию, что добавлен новый пост в категории, на которую подписан пользователь """
    post = Post.objects.get(pk=post_pk)
    categories = post.category.all()
    for category in categories:
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            if subscriber.email:
                # Отправка простого текста
                send_mail(
                    subject=f'{subscriber.email}',
                    message=f'Появился новый пост!\n {post.title}\n {post.text[:50]}.',
                    from_email='kryglov.d@yandex.ru',
                    recipient_list=[subscriber.email, ],
                )
                html_content = render_to_string(
                'mail.html', {
                'user': subscriber,
                'text': f'{post.text[:50]}',
                'post': post.title,
                }
                )
                msg = EmailMultiAlternatives(
                subject=f'Привет, {subscriber.username}. Новая статья в твоём любимом разделе!',
                from_email='kryglov.d@yandex.ru',
                to=[subscriber.email,],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

