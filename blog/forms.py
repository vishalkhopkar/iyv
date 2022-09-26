from django import forms

class RegisterForm(forms.Form):
    emailId = forms.EmailField(label="Email id", widget=forms.EmailInput(attrs={'class': "form-control form-control-lg"}))
    name = forms.CharField(label="Name", max_length=50, widget=forms.TextInput(attrs={'class': "form-control form-control-lg"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control form-control-lg"}), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control form-control-lg"}), label="Confirm Password")

class LoginForm(forms.Form):
    lgn_emailId = forms.EmailField(label="Email id",
                               widget=forms.EmailInput(attrs={'class': "form-control form-control-lg"}))
    lgn_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control form-control-lg"}),
                               label="Password")