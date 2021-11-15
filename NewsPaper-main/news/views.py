from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from . import tasks
import datetime
from django.core.cache import cache
from django.views.decorators.cache import cache_page


class SubscribeView(LoginRequiredMixin, View):
    def get(self, request, category_id, *args, **kwargs):
        user = self.request.user
        category = Category.objects.get(pk=category_id)
        if not category.subscribers.filter(pk=user.pk):
            is_subscriber = False
            category.subscribers.add(user)
        else:
            is_subscriber = True

        context = {
            'categories': Category.objects.all(),
            'category': Category.objects.get(pk=category_id),
            'is_subscriber': is_subscriber
        }
        return render(request, 'subscribe_category.html', context)


class PostsList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_query_data(self, **kwargs):
        query = super().get_context_data(**kwargs)
        query['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_amount'] = len(Post.objects.all())
        context['categories'] = Category.objects.all()
        return context

class PostsCategory(PostsList):
    template_name = 'news/news_category.html'

    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs['category_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = None
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'news_search'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_amount'] = len(Post.objects.all())
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news/news_.html'
    context_object_name = 'news_'
    queryset = Post.objects.all()


    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(**kwargs)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['post_categories'] = self.model.category
        return context


class PostAdd(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/news_add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        user = request.user
        author = Author.objects.get(account=user)

        last_24_hours_posts = Post.objects.filter(author=author, time_of_creation__gt=datetime.date.today())
        if last_24_hours_posts.count() >= 3:
            return redirect('/users/34/')

        post_categories = request.POST.getlist('category')
        post = Post(
            author=author,
            post_type=request.POST['post_type'],
            title=request.POST['title'],
            text=request.POST['text']
        )
        post.save(ctg=post_categories)

        return redirect('/news/')


class PostEdit(PermissionRequiredMixin, UpdateView):
    template_name = 'news/news_edit.html'
    model = Post
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'news/news_delete.html'
    context_object_name = 'news_'
    model = Post
    queryset = Post.objects.all()
    permission_required = ('news.delete_post',)
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def filter_post(request):
    f = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'search.html', {'filter': f})


class Subscribe(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        user = request.user
        category = get_object_or_404(Category, id=kwargs['pk'])
        if category.subs.filter(username=request.user).exists():
            category.subs.remove(user)
        else:
            category.subs.add(user)

        return redirect(request.META['HTTP_REFERER'])