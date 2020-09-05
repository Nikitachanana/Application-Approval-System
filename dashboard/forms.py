from django import forms



class SignUp(forms.Form):
    Aname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'id': 'inputLastName', 'placeholder': 'Enter your name'}))
    Aphone = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'id': 'inputPhone', 'placeholder': 'Enter your phone number'}))
    Aemail = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'id': 'inputEmailAddress', 'placeholder': 'Enter your email'}))
    Auser = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'id': 'inputUsername', 'placeholder': 'Enter your desired username'}))
    Apass = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class': 'form-control py-4', 'id': 'inputPassword', 'placeholder': 'Enter your desired password', 'type': 'password'}))


class SignIn(forms.Form):
    Lemail = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'id': 'emailLogin', 'placeholder': 'Enter your email'}))
    Lpass = forms.CharField(max_length=32, widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'id': 'passLogin', 'placeholder': 'Enter your password',
               'type': 'password'}))


class AdminReg(forms.Form):
        OPTIONS = (
            ("4", "Read"),
            ("2", "Write"),
            ("1", "Execute")
        )
        ACCESS = [
            ('developers', 'Developers'),
            ('marketing', 'Marketing'),
            ('bidding', 'Bidding'),
        ]
        name = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'id': 'inputLastName', 'placeholder': 'Enter your name'}))
        phone = forms.IntegerField(widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'id': 'inputPhone', 'placeholder': 'Enter your phone number'}))
        email = forms.EmailField(widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'id': 'inputEmailAddress', 'placeholder': 'Enter your email'}))
        username = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'id': 'inputUsername', 'placeholder': 'Enter your desired username'}))
        password = forms.CharField(max_length=32, widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'id': 'inputPassword', 'placeholder': 'Enter your desired password',
                   'type': 'password'}))
        perms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)
        team = forms.CharField(widget=forms.RadioSelect(choices=ACCESS))


class Edit(forms.Form):
    OPTIONS = (
        ("4", "Read"),
        ("2", "Write"),
        ("1", "Execute")
    )
    ACCESS = [
        ('developers', 'Developers'),
        ('marketing', 'Marketing'),
        ('bidding', 'Bidding'),
    ]
    # from .models import UserDetails
    a = "Edit Name"
    Eusername = forms.CharField(widget=forms.HiddenInput(
            attrs={'class': 'form-control py-4', 'id': 'ID','readonly':'readonly'}))
    Ename = forms.CharField(label="Enter New Name", widget=forms.TextInput(
            attrs={'class': 'form-control py-4', 'id': 'inputLastName', 'placeholder': a}))
    Ephone = forms.IntegerField(label="Enter New Number", widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'id': 'inputPhone', 'placeholder': 'Edit phone number'}))
    Eemail = forms.EmailField(label="Enter New Email", widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'id': 'inputEmailAddress', 'placeholder': 'Edit email'}))
    # Euser = forms.CharField(label="Enter New Username", widget=forms.TextInput(
    #     attrs={'class': 'form-control py-4', 'id': 'inputUsername', 'placeholder': 'Edit username'}))
    Epass = forms.CharField(label="Enter New Password", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control py-4', 'id': 'inputPassword', 'placeholder': 'Edit password',
               'type': 'password'}))
    Eteam = forms.CharField(label="Select new team", widget=forms.RadioSelect(choices=ACCESS))
    Eperms = forms.MultipleChoiceField(label="Select new permissions", widget=forms.CheckboxSelectMultiple, choices=OPTIONS)

class UserForm(forms.Form):
    title = forms.CharField(label="title",max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description'}))
    picture = forms.ImageField()

class Remark(forms.Form):
    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Enter your remarks',
                                                          'required': False }))