from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Thesis, Group




class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1','password2','user_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': field.label  # Optional: set placeholder as the label text
            })

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128)

class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = ['title', 'description']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'members', 'thesis']


#Error was here
class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, initial=1)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'user_type')

class CustomUserChangeForm(UserChangeForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'email', 'user_type')
