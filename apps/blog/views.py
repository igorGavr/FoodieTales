from wsgiref.util import request_uri
from django.shortcuts import render

from django.views.generic import TemplateView, ListView, DetailView, FormView

from apps.blog.models import Category, Post


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

        return context


from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PostCreateForm


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


