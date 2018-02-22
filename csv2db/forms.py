from django import forms

class searchform(forms.Form):
	symbol	=	forms.CharField(max_length=10)