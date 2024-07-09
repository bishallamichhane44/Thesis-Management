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
        fields = ['title', 'description','category','software_engineering','Information_Systems_and_Data_Science','Mechanical_Engineering','Civil_and_Structural_Engineering','Chemical_Engineering','External','Internal_Sydney','Internal_Casuarina']

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
        
#for delete and edit 


class ThesisForm(forms.ModelForm):
    # Define tag fields as BooleanFields
    software_engineering = forms.BooleanField(required=False, label="Software Engineering")
    Information_Systems_and_Data_Science = forms.BooleanField(required=False, label="Information Systems and Data Science")
    Mechanical_Engineering = forms.BooleanField(required=False, label="Mechanical Engineering")
    Civil_and_Structural_Engineering = forms.BooleanField(required=False, label="Civil and Structural Engineering")
    Chemical_Engineering = forms.BooleanField(required=False, label="Chemical Engineering")
    External = forms.BooleanField(required=False, label="External")
    Internal_Sydney = forms.BooleanField(required=False, label="Internal Sydney")
    Internal_Casuarina = forms.BooleanField(required=False, label="Internal Casuarina")

    class Meta:
        model = Thesis
        fields = ['title', 'description', 'software_engineering', 'Information_Systems_and_Data_Science', 
                  'Mechanical_Engineering', 'Civil_and_Structural_Engineering', 'Chemical_Engineering', 
                  'External', 'Internal_Sydney', 'Internal_Casuarina']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500',
                'placeholder': 'Enter thesis title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Enter thesis description'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(ThesisForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field], forms.BooleanField):
                self.fields[field].widget.attrs.update({
                    'class': 'form-checkbox h-5 w-5 text-blue-600',
                })