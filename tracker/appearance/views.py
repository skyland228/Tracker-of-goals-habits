from .forms import CreateTheme
from .models import Theme
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateTheme(LoginRequiredMixin, CreateView):
    model = Theme
    template_name = 'theme.html'
    form_class = CreateTheme
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
