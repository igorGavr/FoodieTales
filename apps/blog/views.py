from wsgiref.util import request_uri

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.views.generic import (
    TemplateView, ListView,
    DetailView, FormView, UpdateView, CreateView,
)
from apps.blog.models import Category, Post, Comment


# Create your views here.

# CBV - CLass Based Views - Вьюшки на классах
class IndexPage(TemplateView):
    template_name = "index.html"


# Function Based Views - Вьюшки основанные на функциях
# def index_page(request):
#     return render(request,"index.html")


class ProductsView(TemplateView):
    template_name = "products.html"


class CategoryListView(ListView):
    template_name = "category_list.html"
    model = Category
    queryset = Category.objects.all()
    # В шаблоні наш queryset доступний в зміні object_list


# опис вюшки у вигляді функції
# def get_categories(request):
#     categories = Category.objects.all()
#     context = {
#         "categories": categories
#     }
#     return render(request, 'category_list.html', context)


class PostListView(ListView):
    template_name = "post_list.html"
    model = Post
    queryset = Post.objects.filter(is_draft=False)

    # Передаваємо останні пости та категорії в контексті
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Post.objects.filter(is_draft=False).order_by("-created")
        if len(latest_posts) < 4:
            context["latest_posts"] = latest_posts
        else:
            context["latest_posts"] = latest_posts[:3]

        context["categories"] = Category.objects.all()
        return context

    # Переоприділяємо метод get_queryset
    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        # Якщо користувач передає category_slug то ми фільтруємо queryset по ньому
        if category_slug:
            queryset = Post.objects.filter(is_draft=False, category__slug=category_slug)
            return queryset
        # в іншому випадку повертаємо всі пости
        return Post.objects.filter(is_draft=False)


class PostDetailView(DetailView):
    template_name = "post_detail.html"
    model = Post

    # В шаблоні наш запис доступний в зміні object

    # переоприділяємо context та додаємо туди дані для відображення
    # останніх постів та категорій
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Post.objects.filter(is_draft=False).order_by("-created")
        if len(latest_posts) < 4:
            context["latest_posts"] = latest_posts
        else:
            context["latest_posts"] = latest_posts[:3]

        context["categories"] = Category.objects.all()
        # відправляємо форму на сторінку 'blog/post/details'
        context["comment_form"] = CommentCreateForm()

        return context


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PostCreateForm, CommentCreateForm


# LoginRequiredMixin дозволяє мати доступ тільки залогіненим юзерам
class PostCreateView(LoginRequiredMixin, FormView):
    model = Post
    template_name = "post_create.html"
    # підключаємо нашу форму
    form_class = PostCreateForm
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')

    # цей метод спрацює перед зберіганням форми в базу
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class AuthorPostsListView(LoginRequiredMixin, ListView):
    template_name = "author_posts.html"
    model = Post

    def get_queryset(self):
        qs = Post.objects.filter(author=self.request.user)
        return qs

    # переоприділяємо context та додаємо туди дані для відображення
    # останніх постів та категорій
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_posts = Post.objects.filter(is_draft=False).order_by("-created")
        if len(latest_posts) < 4:
            context["latest_posts"] = latest_posts
        else:
            context["latest_posts"] = latest_posts[:3]
        context["categories"] = Category.objects.all()
        return context


def delete_author_post(request, pk):
    # try:
    #     post = Post.objects.get(id=pk)
    # except Post.DoesNotExist:
    #     raise Http404
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect(reverse_lazy("author_posts"))


def deactivate_author_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.is_draft = True
    # update_fields=["is_draft"] - для оптимізації апдейту
    post.save(update_fields=["is_draft"])
    return redirect(reverse_lazy("author_posts"))


def activate_author_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.is_draft = False
    # update_fields=["is_draft"] - для оптимізації апдейту
    post.save(update_fields=["is_draft"])
    return redirect(reverse_lazy("author_posts"))


class PostUpdateView(LoginRequiredMixin, UpdateView):
    # наша форма
    form_class = PostCreateForm
    template_name = "post_create.html"
    model = Post
    success_url = reverse_lazy("author_posts")


# # опис вюшки у вигляді функції
# def update_post(request, pk):
#     post = get_object_or_404(Post, id=pk)
#     if request.method == "GET":
#         # повертаємо заповнену форму
#         form = PostCreateForm(instance=post)
#         context = {
#             "form": post
#         }
#         return render(request, 'post_create.html', context)
#     elif request.method == "POST":
#         form = PostCreateForm(
#             request.POST,
#             request.FILES,
#             instance=post #
#             )
#         if form.is_valid():
#             form.save()
#             return redirect(reverse_lazy("author_posts"))
#         context = {
#             "form":form
#         }
#         return render(request, "post_create.html", context)


# вюшка для створення коментів
# сюди приходять дані з форми з 'post_details.html'
class CommentCreateView(LoginRequiredMixin, FormView):
    form_class = CommentCreateForm
    model = Comment

    def form_valid(self, form):
        # з силки path('comment/create/<int:post_id>/' дістаємо post_id
        post_id = self.kwargs.get("post_id")
        # шукаємо пост
        post = get_object_or_404(Post, id=post_id)
        comment = form.save(commit=False)
        # додаємо автора поста
        comment.author = self.request.user
        # додаємо пост
        comment.post = post
        comment.save()
        return super().form_valid(form)

    # після успішного збереження комента перенаправляємо юзера на
    # сторінку --> path('comment/create/<int:post_id>/'
    # в kwargs передаємо pk поста
    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={'pk': self.kwargs.get('post_id')})

