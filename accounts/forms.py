from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    email = forms.CharField(min_length=3, widget=forms.EmailInput(attrs={
            'placeholder': 'Email...',
            'class': 'form-control form-control-lg'
        })
    )
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control form-control-lg'
    }), label="Password")
    confirm_password = forms.CharField(min_length=4, widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control form-control-lg'
    }), label="Confirm Password")
    username = forms.CharField(min_length=3, widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control form-control-lg'
        })
    )
    first_name = forms.CharField(min_length=3, widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'form-control form-control-lg'
        })
    )
    last_name = forms.CharField(min_length=3, widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'form-control form-control-lg'
        })
    )

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("password and confirm password is not same")
        if len(password) < 4:
            raise forms.ValidationError('Password must be 4 at least')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.staff = True
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password', 'first_name', 'last_name']
