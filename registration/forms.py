from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from .models import User
from django import forms
from django.urls import reverse_lazy


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set class attribute for styling
        for field_name in self.fields:
            self.fields[field_name].widget.attrs["class"] = "form-control"

        # Set autofocus on the email field
        self.fields['email'].widget.attrs['autofocus'] = True

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(("This username is already in use."))
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
        
        
class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"
        

class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields['password'].help_text = (
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            '<a href="{}">this form</a>.'.format(reverse_lazy('registration:change_password'))
        )


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "type":"password"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "type":"password"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "type":"password"}))

    class Meta:
        model = User
        fields = ("old_password", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(PasswordChangingForm, self).__init__(*args, **kwargs)

        self.fields["old_password"].widget.attrs["class"] = "form-control"
        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["class"] = "form-control"



