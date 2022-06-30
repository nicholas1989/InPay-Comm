from django import forms
#from . models import Customer

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
    
'''  
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'customer_name', 
            'email', 
            'phone_number', 
        )
        
'''         