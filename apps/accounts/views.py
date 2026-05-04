from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import User
from .forms import UserProfileForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return self.request.user


class TeamView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/team.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["owned_teams"] = self.request.user.owned_teams.all()
        ctx["memberships"] = self.request.user.memberships.select_related("team").all()
        return ctx