from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from users.models import User

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=100, help_text='Required.')

	class Meta:
		model = User
		fields = ("email", "username", "password1", "password2")
		
class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'password')

	def clean(self):
		email = self.cleaned_data['email']
		password = self.cleaned_data['password']
		if not authenticate(email=email, password=password):
			raise forms.ValidationError("invalid login")
