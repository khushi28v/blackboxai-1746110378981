from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'border rounded px-3 py-2 w-full'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'border rounded px-3 py-2 w-full', 'rows': 4}))
