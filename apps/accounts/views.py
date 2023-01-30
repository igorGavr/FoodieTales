from django.shortcuts import render, redirect

from django.views.generic import (
    FormView, CreateView, TemplateView, UpdateView,
    ListView, DetailView,
)
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404

from apps.accounts.forms import LoginForm, UserRegisterForm, UserUpdateForm
from apps.accounts.models import User


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    # цей метод спрацьовує лише тоді коли юзер заповнив форму валідними даними та відправив
    def form_valid(self, form):
        data = form.cleaned_data  # {"password":"admin", "email":"admin@gmail.com"}
        # cleaned_data дані у вигляді dict
        print(data)
        email = data["email"]
        password = data["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect("index")
            return HttpResponse("Ваш акаунт не активний")
        return HttpResponse("Введіть коректні дані")


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")


from django.http import HttpResponseRedirect
from apps.accounts.utils import send_activation_email


class UserRegisterView(CreateView):
    template_name = "register.html"
    form_class = UserRegisterForm
    model = User
    success_url = reverse_lazy('register_done')

    # після введення валідних даних спрацьовує цей метод
    def form_valid(self, form):
        # поки що не зберігаємо користувача
        user = form.save(commit=False)
        # робимо користувача не активним
        user.is_active = False
        user.save()
        send_activation_email(user, request=self.request, to_email=user.email)
        return super().form_valid(form)


class RegisterDoneView(TemplateView):
    template_name = "register_done.html"


from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator


def activate_account(request, uidb64, token):
    try:
        # дешифруємо айдішку юзера
        uid = int(force_str(urlsafe_base64_encode(uidb64)))
        user = User.objects.get(id=uid)
    except (ValueError, User.DoesNotExist, TypeError):
        user = None
    # перевірка юзера та токена
    if user is not None and default_token_generator.check_token(user, token):
        # якщо перевірка пройшла то робимо юзера активним
        user.is_active = True
        # логінимо цього юзера
        login(request, user)
        # та редіректимо на головну сторінку
        return redirect(reverse_lazy('index'))
    # якщо перевірка не проходить то вибиває помилка
    raise Http404


class UpdateUserView(UpdateView):
    template_name = "profile.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy("index")

    def get_object(self):
        return self.request.user


class AllUsersView(ListView):
    model = User
    template_name = "users.html"


class UsersSearchListView(ListView):
    template_name = "users.html"
    model = User

    def get_queryset(self):
        search_text = self.request.GET.get("query")
        if search_text:
            search_users = User.objects.filter(first_name__icontains=search_text)
            return search_users
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_text"] = self.request.GET.get("query")
        return context


class UserDetailView(DetailView):
    model = User
    template_name = "user_details.html"

