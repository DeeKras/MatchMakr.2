from django import forms
from django.contrib.auth.models import User
from django.forms import  Textarea, TextInput

from .models import Advocate, Single, AdvocateChangeLog, SingleChangeLog
from .utils import get_ip


class AuthenticationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.widgets.TextInput, label="User Name")
    password = forms.CharField(widget=forms.widgets.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['username', 'password', ]

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.widgets.TextInput, label="First Name")
    last_name = forms.CharField(widget=forms.widgets.TextInput, label="Last Name")
    email = forms.EmailField(widget=forms.widgets.TextInput, label="Email")

    username = forms.CharField(widget=forms.widgets.TextInput, label="User Name", required=True)
    password1 = forms.CharField(widget=forms.widgets.PasswordInput, label="Password", required=True)
    password2 = forms.CharField(widget=forms.widgets.PasswordInput, label="Password (again)", required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #     self.fields['password1'].required = False
    #     self.fields['password2'].required = False

    def clean(self):
        self.cleaned_data = super(UserForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

class AdvocateForm(forms.ModelForm):
    city = forms.CharField(widget=forms.widgets.TextInput, label="City")
    state = forms.CharField(widget=forms.widgets.TextInput, label="State/ Province")
    country = forms.CharField(widget=forms.widgets.TextInput, label="Country")
    phone = forms.CharField(widget=forms.widgets.TextInput, label="Phone")

    class Meta:
        model = Advocate
        fields = ['city', 'state','country', 'phone']

class AdvocateSignupForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.widgets.TextInput, label="First Name")
    last_name = forms.CharField(widget=forms.widgets.TextInput, label="Last Name")

    username = forms.CharField(widget=forms.widgets.TextInput, label="User Name")
    password1 = forms.CharField(widget=forms.widgets.PasswordInput, label="password")
    password2 = forms.CharField(widget=forms.widgets.PasswordInput, label="password (again)")

    city = forms.CharField(widget=forms.widgets.TextInput, label="City")
    state = forms.CharField(widget=forms.widgets.TextInput, label="State/ Province")
    country = forms.CharField(widget=forms.widgets.TextInput, label="Country")
    email = forms.EmailField(widget=forms.widgets.TextInput, label="Email")
    phone = forms.CharField(widget=forms.widgets.TextInput, label="Phone")

    def clean(self):
        self.cleaned_data = super(AdvocateSignupForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self):
        user = User.objects.create_user(self.cleaned_data['username'],
                                        self.cleaned_data['email'],
                                        self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        advocate = Advocate.objects.create(user=user,
                                           city=self.cleaned_data['city'],
                                           state=self.cleaned_data['state'],
                                           country=self.cleaned_data['country'],
                                           phone=self.cleaned_data['phone'],
                                           how_added='user added')
        advocate.save()
        return user

    def save_change(self, request, pk):
        user = User.objects.get(pk=pk)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        advocate = Advocate.object.get(pk=user.pk)
        advocate.city=self.cleaned_data['city']
        advocate.state=self.cleaned_data['state']
        advocate.country=self.cleaned_data['country']
        advocate.phone=self.cleaned_data['phone']
        advocate.save()

        advocate_change = AdvocateChangeLog.objects.create(user=user,
                                           city=self.cleaned_data['city'],
                                           state=self.cleaned_data['state'],
                                           country=self.cleaned_data['country'],
                                           phone=self.cleaned_data['phone'],
                                           ip_of_change=get_ip(request))
        advocate_change.save()


class SingleProfileForm(forms.ModelForm):
    class Meta:
        model = Single
        fields = ['first_name', 'last_name','gender', 'age', 'photo','resume',
                  'how_advocate_knows', 'reference', 'prefered_matchmaker', 'short_desc' ]

class EditEmailForm(forms.Form):
    single_id = forms.IntegerField()
    email_to = forms.CharField(label='To',  widget=forms.Textarea(
                                    attrs={'rows': 1,
                                            'cols': 120,}))
    email_from = forms.CharField(label='From', widget=forms.Textarea(
                                    attrs={'rows': 1,
                                            'cols': 90, }))
    email_subject = forms.CharField(label='Subject', widget=forms.Textarea(
                                    attrs={'rows': 1,
                                            'cols': 90,}))
    email_body = forms.CharField(label="Message", widget=forms.Textarea(
                                    attrs={'rows': 1,
                                            'cols': 90,
                                            'style': 'height: 15em;'}))
    email_attachment = forms.ImageField(label="Attachment")





