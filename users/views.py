from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.views.generic import CreateView

class RegisterCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('login')

