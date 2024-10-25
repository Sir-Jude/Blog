from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegistrationForm, LoginForm, EditProfileForm, PasswordChangingForm


class UserRegisterView(generic.CreateView):
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")
    

class UserLoginView(generic.FormView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("blog:home")
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    

class UserProfileEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = "registration/edit_profile.html"
    success_url = reverse_lazy("home")
    
    def get_object(self):
        return self.request.user
    
class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        messages.success(self.request, "Your password was successfully updated!")
        return super().form_valid(form)