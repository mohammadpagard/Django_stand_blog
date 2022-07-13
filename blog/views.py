from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment, Message, Like
from django.core.paginator import Paginator
from .forms import MessageForm
from django.views.generic import ListView, DetailView, FormView
from . import mixins as my_mixins


class PostDetail(my_mixins.CustomLoginRequiredMixin, DetailView):
    model = Post
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Post.objects.all(), slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['comment'] = Comment.objects.all()
        context['form'] = Comment()
        # like
        if self.request.user.likes.filter(post__slug=self.object.slug, user_id=self.request.user.id).exists():
            context['is_liked'] = True
        else:
            context['is_liked'] = False

        return context


class PostList(ListView):
    queryset = Post.objects.filter(status=True).order_by('-created',)
    context_object_name = 'object_list'
    paginate_by = 4


class CategoryList(ListView):
    paginate_by = 4
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        return category.posts.all()

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=slug)
        return context


def search(request):
    q = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=q)
    page_number = request.GET.get('page')
    pagiantor = Paginator(posts, 4)
    objects_list = pagiantor.get_page(page_number)

    context = {
        'posts': objects_list,
    }

    return render(request, 'blog/posts_list.html', context)


class ContactUsView(FormView):
    template_name = "blog/contact_us.html"
    form_class = MessageForm
    success_url = "/"


    def form_valid(self, form):
        form_data = form.cleaned_data
        Message.objects.create(**form_data)

        return super().form_valid(form)


def like(request, slug, pk):
    try:
        like = Like.objects.get(post__slug=slug, user_id=request.user.id)
        like.delete()
    except:
        Like.objects.create(post_id=pk, user_id=request.user.id)

    return redirect('blog:detail', slug)