from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'dateCreation': ['gt'],
            'title': ['icontains'],
            'author__authorUser__username': ['contains'],
        }

