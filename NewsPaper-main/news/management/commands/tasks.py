from django.core.mail import EmailMultiAlternatives
from NewsPaper.news.models import Subscriber, Post, Category
from django.template.loader import render_to_string
import datetime


def weekly_notifications():
    categories = Category.objects.all()
    for category in categories:
        posts = Post.objects.filter(category=category, time_of_creation__gt=datetime.date.today() - datetime.timedelta(weeks=1))
        subs = Subscriber.objects.filter(category=category)
        for sub in subs:
            html_content = render_to_string(
                    'mail.html',
                    {
                        'sub': sub.user.username,
                        'posts': posts,
                        'category': category.title
                    }
                )
            msg = EmailMultiAlternatives(
                subject=f"Posts in {category.title} per week!",
                body='example',
                from_email='kryglov.d@yandex.ru',
                to=[sub.user.email]
            )
            msg.attach_alternative(html_content, "text/html")

            msg.send()