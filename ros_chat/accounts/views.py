from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login

from .forms import CustomUserCreationForm


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


def do_logout(request):
    """Просит пользователя ещё раз подтвердить, что он хочет выйти из системы.
    Если пользователь подтверждает, то происходит выход (logout).
    """
    template = 'logout.html' if not request.htmx else 'part/logout_content.html'
    return render(request, template)