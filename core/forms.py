from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Insert your name"
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Your email"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Your message"
    }))