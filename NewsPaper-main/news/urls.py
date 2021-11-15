from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostAdd, PostEdit, PostDelete, PostsCategory, SubscribeView

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='news_'),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('add/', PostAdd.as_view(), name='news_add'),
    path('edit/<int:pk>', PostEdit.as_view(), name='news_edit'),
    path('delete/<int:pk>', PostDelete.as_view(), name='news_delete'),
    path('category/<int:category_id>', PostsCategory.as_view(), name='news_category'),
    path('category/<int:category_id>/subscribe', SubscribeView.as_view(), name='subscribe'),
]
