from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import  reverse_lazy
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import  Textarea, TextInput
from django.forms.models import modelform_factory
import os

from .forms import  AuthenticationForm, SingleProfileForm, UserForm, AdvocateForm
from .models import Single, SingleChangeLog, Circle, Advocate
from .utils import create_profile_image
from .email import profile_to_friend, process_email, edit_email
from mysite.settings import BASE_DIR

class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


def home(request):
    return render_to_response('matches/home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/advocate')
        else:
            form = AuthenticationForm(request.POST)

    else:
        form = AuthenticationForm()

    template_name = 'matches/login.html'
    return render(request, template_name, {'form': form})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def advocate_homepage(request):
    users_singles = Single.objects.filter(created_by=request.user).order_by('last_name', 'first_name')

    template_name = 'matches/advocate_homepage.html'
    context = {'user': request.user, 'singles': users_singles}
    return render(request, template_name, context)


def advocate_signup(request):

    if request.method == 'POST':
        userform = UserForm(data=request.POST)
        advocateform = AdvocateForm(data=request.POST)

        if userform.is_valid():
            if 'password1' in userform.cleaned_data and 'password2' in userform.cleaned_data:
                if userform.cleaned_data['password1'] != userform.cleaned_data['password2']:
                    raise forms.ValidationError("Passwords don't match. Please enter both fields again.")

            user = User.objects.create_user(userform.cleaned_data['username'],
                                        userform.cleaned_data['email'],
                                        userform.cleaned_data['password1'])
            user.first_name = userform.cleaned_data['first_name']
            user.last_name = userform.cleaned_data['last_name']
            user.save()


            if advocateform.is_valid():
                advocate = Advocate.objects.create(user=user,
                                               city=advocateform.cleaned_data['city'],
                                               state=advocateform.cleaned_data['state'],
                                               country=advocateform.cleaned_data['country'],
                                               phone=advocateform.cleaned_data['phone'],
                                               how_added='user added')
                advocate.save()

                return HttpResponseRedirect('/login')

    else:
        userform = UserForm()
        advocateform = AdvocateForm()

    template_name = 'matches/advocate_new_form.html'
    return render(request, template_name, {'userform': userform, 'advocateform': advocateform})

def update_advocate(request, pk):
    # advocate = User.objects.get(pk=pk).advocate
    user = User.objects.get(pk=pk)
    advocate = Advocate.objects.get(user_id=pk)
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=user)
        advocateform = AdvocateForm(request.POST, instance=advocate)

        if userform.is_valid():
            userform.save()
        # else:
        #     TODO: need something here
        if advocateform.is_valid():
        # else:
        #     TODO: need something here
            advocateform.save()
        return redirect('advocate_homepage')
    else:
        userform = UserForm(instance=user)
        advocateform = AdvocateForm(instance=advocate)
        my_circles = Circle.objects.filter(advocate__pk=advocate.pk)

        template_name = 'matches/advocate_change_form.html'
        context = {'user': request.user, 'userform': userform, 'advocateform': advocateform, 'pk': pk, 'my_circles':my_circles}
        return render(request, template_name, context)

@login_required
def search_circles_form(request):
    advocate = Advocate.objects.get(user=request.user)
    user_circles = Circle.objects.filter(advocate__pk=advocate.pk)

    template_name = 'matches/advocate_circles_form.html'
    context = {'user': request.user, 'circles':user_circles}
    return render(request, template_name, context)


@login_required
def add_to_circle_form(request):
    template_name = 'matches/add_to_circle_form.html'
    context = {'user': request.user }
    return render(request, template_name, context)


def add_circle(request):
    advocate = Advocate.objects.get(user=request.user)
    circle = Circle.objects.get(code=request.POST['circle'])
    advocate.circles.add(circle.pk)
    circle.members.add(advocate.user.pk)
    return redirect('advocate_homepage')


@login_required
def show_circle_list(request):
    circle = Circle.objects.get(pk=request.POST['circle'])
    singles = Single.objects.filter(created_by__circle=circle.pk, gender=request.POST['gender'])\
                        .order_by('last_name', 'first_name')


    template_name = 'matches/list_singles_in_circle.html'
    context = {'user': request.user, 'circle': circle.name,
               'gender': request.POST['gender'], 'singles': singles}
    return render(request, template_name, context)


@login_required
def display_single_profile(request, pk):
    single = Single.objects.get(pk=pk)
    template_name = 'matches/single_profile.html'
    context = {'user': request.user,'single': single}
    return render_to_response(template_name, context)


class SingleCreate(ModelFormWidgetMixin, CreateView):
    model = Single
    fields = ['first_name', 'last_name','gender', 'age', 'how_advocate_knows',
              'photo', 'resume', 'reference', 'prefered_matchmaker', 'short_desc',
              'father', 'mother', 'parents_location']
    widgets = {
            'first_name': TextInput(attrs={'placeholder': "First Name/ Commonly Called"}),
            'mother': TextInput(attrs={'placeholder': "First Name, Last Name [Maiden Name]"}),
            'short_desc':Textarea(attrs={'rows': 1, 'cols': 90, 'style': 'height: 10em;',
                                         'placeholder': "Enter a brief description; include something that makes \
                                         him/ her unique (for example: plays a musical instrument, loves to garden, volunteers at children's hospital . \
                                                        This will be seen by anyone logging in to see your singles. (3000 characters max)"}),
            'reference': TextInput(attrs={'placeholder': 'Name & Contact Info'}),
            'prefered_matchmaker': TextInput(attrs={'placeholder': 'Name & Contact Info'}),
            'how_advocate_knows': Textarea(attrs={'placeholder': "I am this person's [mother/ father/ co-worker/ friend/ neighbor/ etc.]"})
        }
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.most_recent_change_id = 0
        self.object.save()

        single = get_object_or_404(Single, pk=self.object.pk)

        f =SingleChangeLog(single = single,
                                 first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'],
                                 age=form.cleaned_data['age'],
                                 gender=form.cleaned_data['gender'],
                                 photo=form.cleaned_data['photo'],
                                 changed_by=self.request.user)
        f.save()

        self.profile_name = create_profile_image(single.pk)
        self.object.profile_image = self.profile_name
        self.object.save()

        return redirect('advocate_homepage')


class SingleUpdate(ModelFormWidgetMixin, UpdateView):
    model = Single
    fields = ['first_name', 'last_name','gender', 'age', 'how_advocate_knows',
              'photo', 'resume', 'reference', 'prefered_matchmaker', 'short_desc',
              'father', 'mother', 'parents_location']
    widgets = {
            'first_name': TextInput(attrs={'placeholder': "First Name/ Commonly Called"}),
            'mother': TextInput(attrs={'placeholder': "First Name, Last Name [Maiden Name]"}),
            'short_desc':Textarea(attrs={'rows': 1, 'cols': 90, 'style': 'height: 10em;',
                                         'placeholder': "Enter a brief description; include something that makes \
                                         him/ her unique (for example: plays a musical instrument, loves to garden, volunteers at children's hospital . \
                                                        This will be seen by anyone logging in to see your singles. (3000 characters max)"}),
            'reference': TextInput(attrs={'placeholder': 'Name & Contact Info'}),
            'prefered_matchmaker': TextInput(attrs={'placeholder': 'Name & Contact Info'}),
            'how_advocate_knows': Textarea(attrs={'placeholder': "I am this person's [mother/ father/ co-worker/ friend/ neighbor/ etc.]"})
        }
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        single = get_object_or_404(Single, pk=self.object.pk)
        if single.profile_image != 'profile_jpgs/None/no-img.jpg':
            to_delete = '{}/media/profile_jpgs/{}'.format(BASE_DIR, single.profile_image)
            os.remove(to_delete)

        profile_name = create_profile_image(single.pk)
        self.object.profile_image = profile_name
        self.object.save()

        f =SingleChangeLog(single=single,
                             first_name = form.cleaned_data['first_name'],
                             last_name = form.cleaned_data['last_name'],
                             age = form.cleaned_data['age'],
                             gender = form.cleaned_data['gender'],
                             photo = form.cleaned_data['photo'],
                             profile_image=profile_name,
                             changed_by=self.request.user)
        f.save()
        return redirect('advocate_homepage')



def update_single(request, pk):
    single = get_object_or_404(Single, pk=pk)
    if request.method == 'POST':
        form = SingleProfileForm(request.POST, request.FILES, instance=single)

        if form.is_valid():
            form.save()

            if single.profile_image != 'profile_jpgs/None/no-img.jpg':
                to_delete = '{}/media/profile_jpgs/{}'.format(BASE_DIR, single.profile_image)
                os.remove(to_delete)

            profile_name = create_profile_image(single.pk)
            single.profile_image = profile_name
            single.save()

            f =SingleChangeLog(single=single,
                                 first_name = form.cleaned_data['first_name'],
                                 last_name = form.cleaned_data['last_name'],
                                 age = form.cleaned_data['age'],
                                 gender = form.cleaned_data['gender'],
                                 photo = form.cleaned_data['photo'],
                                 profile_image=profile_name,
                                 changed_by=request.user)
            f.save()
            return redirect('advocate_homepage')
        else:
            form = SingleProfileForm(instance=single)
            template_name = 'matches/single_form.html'
            context = {'user': request.user, 'form': form, 'single': single, 'mode': 'update'}
            return render(request, template_name, context)


    else:
        form = SingleProfileForm(instance=single)
        template_name = 'matches/single_form.html'
        context = {'user': request.user, 'form': form, 'single': single, 'mode': 'update'}
        return render(request, template_name, context)

@login_required
def single_search_form(request):
    my_singles = Single.objects.filter(created_by=request.user)
    advocate = Advocate.objects.get(user=request.user)
    my_circles = Circle.objects.filter(advocate__pk=advocate.pk)

    template_name = 'matches/search_single_form.html'
    context = {'user': request.user, 'my_singles': my_singles, 'circles': my_circles}
    return render(request, template_name, context)


def search_single(request):
    if request.POST:
        single = Single.objects.get(pk=request.POST['single'])
        form = SingleProfileForm(instance=single)
        template_name = 'matches/single_form.html'
        context = {'form': form, 'single': single}
        pk=single.pk
        return redirect('single_edit', pk=pk)
        # return render(request, template_name, context)
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)


def edit_single_profile(request, pk):
    single = get_object_or_404(Single, pk=pk)
    email_data = profile_to_friend(request, single)
    return edit_email(request, email_data)

@login_required
def send_email(request):
    attachment = 'media/profile_jpgs/{}'.format(Single.objects.get(id=request.POST['single_id']).profile_image)
    email_data = {'from': request.POST['email_from'],
                    'to': request.POST['to'],
                    'subject': request.POST['email_subject'],
                    'text': request.POST['email_body']}
    process_email(email_data, attachment)
    return redirect('advocate_homepage')

