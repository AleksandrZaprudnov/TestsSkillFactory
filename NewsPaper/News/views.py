from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post
from .filters import NewsFilter
from .forms import NewsModelForm


class PostsListView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-datetime_created')
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsSearchList(ListView):
    model = Post
    template_name = 'news/search/posts_list.html'
    context_object_name = 'posts'
    ordering = '-datetime_created'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # print(self.request.GET)
        context = super().get_context_data(**kwargs)
        # print(context)
        filtered = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = filtered

        paginated_filtered_persons = Paginator(filtered.qs, self.paginate_by)
        page_number = self.request.GET.get('page')
        person_page_object = paginated_filtered_persons.get_page(page_number)
        context['person_page_object'] = person_page_object

        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'News.add_post'
    per = 'News.add_post'
    template_name = 'news/post_create.html'
    form_class = NewsModelForm


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'News.change_post'
    template_name = 'news/post_update.html'
    form_class = NewsModelForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

