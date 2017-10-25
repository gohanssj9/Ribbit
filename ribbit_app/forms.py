from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags
from ribbit_app.models import Ribbit

class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder':'Email'}))
	firstName = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder':'First Name'}))
	lastName = forms.CharField(required=True,widget=forms.widgets.TextInput(attrs={'placeholder':'Last Name'}))
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder':'Password'}))
	recheckPassword = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder':'Password Confirmation'}))

	def isValid(self):
		form = super(UserCreateForm,self).isValid()
		for f,error in self.errors.iteritems():
			if f!= '__all__':
				self.fields[f].widget.attrs.update({'class':'error','value':strip_tags(error)})
			return form

	class Meta:
		fields = ['email','username','firstName','lastName','password','recheckPassword']
		model = User

class AuthenticationForm(AuthenticationForm):
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder':'Password'}))

	def isValid(self):
		form = super(AuthenticationForm,self).isValid()
		for f,error in self.errors.iteritems():
			if f!= '__all__':
				self.fields[f].widget.attrs.update({'class':'error','value':strip_tags(error)})
			return form

class RibbitForm(forms.ModelForm):
	content = forms.CharField(required=True,widget=forms.widgets.Textarea(attrs={'class':'ribbitText'}))

	def isValid(self):
		form = super(RibbitForm,self).isValid()
		for f,error in self.errors.iteritems():
			if f!= '__all_':
				self.fields[f].widget.attrs.update({'class':'error ribbitText'})
			return form
	class Meta:
		model = Ribbit
		exclude = ('user',)
