from django import forms

class InstagramUserForm(forms.Form):
	username = forms.CharField(label='Instagram username', max_length=100)