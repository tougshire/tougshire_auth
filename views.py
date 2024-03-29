from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, RedirectURLMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .models import TougshireAuthUser
from .forms import ProfileForm, RegisterForm
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib import messages


class ProfileDetail(DetailView):
    model = TougshireAuthUser
    template_name = "tougshire_auth/profile_detail.html"

    def get_object(self):
        if self.request.user.pk:
            return self.request.user
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if hasattr(settings, "TOUGSHIRE_AUTH_MENU_FILE"):
            context_data["menufile"] = settings.TOUGSHIRE_AUTH_MENU_FILE

        return context_data


class ProfileUpdate(UpdateView):
    model = TougshireAuthUser
    template_name = "tougshire_auth/profile_form.html"
    form_class = ProfileForm

    def get_object(self):
        if self.request.user.pk:
            return self.request.user
        raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy("tougshire_user_profile")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if hasattr(settings, "TOUGSHIRE_AUTH_MENU_FILE"):
            context_data["menufile"] = settings.TOUGSHIRE_AUTH_MENU_FILE

        return context_data


class LoginView(LoginView):
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["allow_registration"] = (
            hasattr(settings, "TOUGSHIRE_AUTH")
            and "allow_registration" in settings.TOUGSHIRE_AUTH
            and settings.TOUGSHIRE_AUTH["allow_registration"] == True
        )
        return context_data


class RegistrationView(RedirectURLMixin, CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "tougshire_auth/register.html"

    def dispatch(self, request, *args, **kwargs):
        allow_registration = (
            hasattr(settings, "TOUGSHIRE_AUTH")
            and "allow_registration" in settings.TOUGSHIRE_AUTH
            and settings.TOUGSHIRE_AUTH["allow_registration"] == True
        )
        if not allow_registration:
            raise PermissionDenied("Registration is Disabled")

        return super().dispatch(request, *args, **kwargs)


# def register(request):

#     allow_registration = hasattr(settings,'TOUGSHIRE_AUTH') and 'allow_registration' in settings.TOUGSHIRE_AUTH and settings.TOUGSHIRE_AUTH['allow_registration'] == True

#     if allow_registration:
#         if request.method == "POST":
#             form = RegisterForm(request.POST)
#             if form.is_valid():
#                 user=form.save()
#                 return HttpResponseRedirect(reverse('logout'))
#             else:
#                 messages.error(request, "Unsuccessful registration")
#                 for error in form.errors:
#                     messages.error(request, error)
#                     messages.error(request, form.errors[ error ])

#         form = RegisterForm()
#         return render(request, "tougshire_auth/register.html", {"form":form})
#     return HttpResponse('Registration is disabled')
