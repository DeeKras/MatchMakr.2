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
from datetime import datetime

from .forms import  AuthenticationForm, SingleProfileForm, UserForm, AdvocateForm, DeactivateSingleForm
from .models import Single, SingleChangeLog, Circle, Advocate
from .utils import create_profile_image, DEACTIVATE_SINGLES_CHOICES
from .email import create_html_profile_to_friend, create_html_request_resume, process_email, edit_email
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

#Advocate

def advocate_homepage(request):
    '''
    creates Advocate Homepage
    '''
    users_singles = Single.objects.filter(created_by=request.user).order_by('last_name', 'first_name')

    template_name = 'matches/advocate_homepage.html'
    context = {'user': request.user, 'singles': users_singles}
    return render(request, template_name, context)


def advocate_signup(request):
    '''
    user signs up as advocate
    saves new advocate
    '''

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
    '''
    updates Advocate info
    '''
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
def add_to_circle_form(request):
    '''
    Creates the form for advocate to add self to a circle
    '''
    template_name = 'matches/add_to_circle_form.html'
    context = {'user': request.user }
    return render(request, template_name, context)


def add_circle(request):
    '''
    adds the new circle to the Advocate
    '''
    advocate = Advocate.objects.get(user=request.user)
    circle = Circle.objects.get(code=request.POST['circle'])
    advocate.circles.add(circle.pk)
    circle.members.add(advocate.user.pk)
    return redirect('advocate_edit', advocate.user.pk )


#Singles

class SingleCreate(ModelFormWidgetMixin, CreateView):
    '''
    Creates a new Single, including a Single Profile (jpg)
    Creates a record in SingleChangeLog
    '''
    model = Single
    fields = ['first_name', 'last_name','gender', 'age', 'how_advocate_knows',
              'photo', 'resume', 'reference', 'prefered_matchmaker', 'short_desc',
              'father', 'mother', 'parents_location', 'status']
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
        user = self.request.user

        #saves to the SingleChangeLog
        save_SingleChangeLog(single, form, user, status="A")

        #creates a new profile (jpg)
        create_profile_jpg(self, single)

        return redirect('advocate_homepage')


class SingleUpdate(ModelFormWidgetMixin, UpdateView):
    '''
    Updates the Single, replaces the Single Profile (jpg)
    Also creates a new record in the SingleChangeLog
    Then redirects to Advocate Homepage
    '''
    model = Single
    fields = ['first_name', 'last_name','gender', 'age', 'how_advocate_knows',
              'photo', 'resume', 'reference', 'prefered_matchmaker', 'short_desc',
              'father', 'mother', 'parents_location', 'status']
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
        user = self.request.user
        # status =

        #deletes the old profile(jpg) to save space
        if single.profile_image != 'profile_jpgs/None/no-img.jpg':
            to_delete = '{}/media/profile_jpgs/{}'.format(BASE_DIR, single.profile_image)
            os.remove(to_delete)

        #creates a new profile (jpg)
        create_profile_jpg(self, single)

        #saves to the SingleChangeLog
        save_SingleChangeLog(single, form, user, status= form.cleaned_data['status'])

        return redirect('advocate_homepage')

def create_profile_jpg(self, single):
    '''
    creates an jpg of the Single's information & photo
    '''
    profile_name = create_profile_image(single.pk)
    self.object.profile_image = profile_name
    self.object.save()


def save_SingleChangeLog(single, form, user, status):
    '''
    saves a record in the SingleChangeLog
    '''
    f =SingleChangeLog(single=single,
                             first_name = form.cleaned_data['first_name'],
                             last_name = form.cleaned_data['last_name'],
                             age = form.cleaned_data['age'],
                             gender = form.cleaned_data['gender'],
                             photo = form.cleaned_data['photo'],
                             status = status,
                             changed_by=user)
    f.save()


def change_single_status_form(request, pk):
    if request.POST:

        form = DeactivateSingleForm(data=request.POST)

        if form.is_valid():
            single = Single.objects.get(pk=pk)
            single.status = 'I'
            single.save()


            f = SingleChangeLog(single=single,
                             first_name = single.first_name,
                             last_name = single.last_name,
                             age = single.age,
                             gender = single.gender,
                             photo = single.photo,
                             status = 'I',
                             deactivate_date=datetime.now(),
                             deactivate_reason=request.POST['deactivate_reason'],
                             changed_by=request.user)
            f.save()



        else:
            pass # TODO: error trap
        return redirect('advocate_homepage')
    else:
        single = Single.objects.get(pk=pk)
        form = DeactivateSingleForm(single)
        template_name =  'matches/single_change_status_form.html'
        context = {'form': form, 'single': single, 'CHOICES': DEACTIVATE_SINGLES_CHOICES}
        return render(request, template_name, context)


@login_required
def display_single_profile(request, pk):
    '''
    Opens a page with Single's full data
    '''
    single = Single.objects.get(pk=pk)
    template_name = 'matches/single_profile.html'
    context = {'user': request.user,'single': single}
    return render_to_response(template_name, context)

#emails

def email_single_profile(request, pk):
    '''
    Processes the request to "email single's profile"
    Sends the 'single' to   email.'create_html_profile_to_friend'
    receives back the html - as editable form, populated with the email_data
    '''
    single = get_object_or_404(Single, pk=pk)
    email_data = create_html_profile_to_friend(request, single)
    return edit_email(request, email_data)

def email_request_resume(request, pk):
    '''
    Processes the request to "email to request a resume"
    Sends the 'single' to   email.'create_html_request_resume'
    receives back the html - as editable form, populated with the email_data
    '''
    single = get_object_or_404(Single, pk=pk)
    email_data = create_html_request_resume(request, single)
    return edit_email(request, email_data)

@login_required
def send_email(request):
    '''
    Receives back the html - as editable form, populated with the email_data
    when User clicks 'Send', this sends the email_data to email.process_email (which emails it)
    and then redirects to homepage
    '''

    email_data = {'from': request.POST['email_from'],
                    'to': request.POST['email_to'],
                    'subject': request.POST['email_subject'],
                    'text': request.POST['email_body'],
                    'attachment': request.POST['email_attachment']}
    process_email(email_data)
    return redirect('advocate_homepage')

#searches

@login_required
def single_search_form(request):
    '''
    creates the Search for Singles form
    '''
    my_singles = Single.objects.filter(created_by=request.user)
    advocate = Advocate.objects.get(user=request.user)
    my_circles = Circle.objects.filter(advocate__pk=advocate.pk)

    my_circles_list = my_circles.values_list('id', flat=True)
    advocates_in_my_circles = Advocate.objects.filter(circles__pk__in=my_circles_list)\
        .order_by('user__last_name', 'user__first_name').distinct()

    template_name = 'matches/search_single_form.html'
    context = {'user': request.user, 'my_singles': my_singles, 'circles': my_circles, 'advocates': advocates_in_my_circles}
    return render(request, template_name, context)

#search results

def get_search_results(request):
    '''
    When User clicks 'submit' on the 'Search for Singles' page,
    this is accessed. Based on ['submit'], determines how to process the search results.
    '''
    min_age = request.POST['min_age'] if request.POST['min_age'] else 0
    max_age = request.POST['max_age'] if request.POST['max_age'] else 100
    gender = request.POST['gender']

    if gender == "A":
        gender_display = "All"
    elif gender == "M":
        gender_display = "Men"
    else:
        gender_display = "Women"

    if min_age and max_age:
        age_display = '{} - {}'.format(min_age, max_age)
    else:
        age_display = "Any"

    if request.POST['submit'] == 'by_circle':
        if request.POST['circles'] != 'choose a circle':
            return search_results_by_circle(request, min_age, max_age, gender, gender_display, age_display)
        else:
            return HttpResponse('you did not select a Circle') #TODO: replace with proper error message
    elif request.POST['submit'] == 'by_advocate':
        if request.POST['singles_by_advocate'] != 'choose an advocate':
            return search_results_by_advocate(request, min_age, max_age, gender, gender_display, age_display)
        else:
            return HttpResponse('you did not select an Advocate') #TODO: replace with proper error message
    elif request.POST['submit'] == 'my_single':
        return search_results_single(request)

@login_required
def search_results_single(request):
    '''
    Produces the results and then renders the template for search results for 'one of my singles'
    '''
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

@login_required
def search_results_by_circle(request, min_age, max_age, gender, gender_display, age_display):
    '''
    Produces the results and then renders the template for search results for 'singles by circle'
    '''

    circle = Circle.objects.get(pk=request.POST['circles'])
    singles = Single.objects.filter(created_by__circle=circle.pk)\
                            .filter(age__range=(min_age, max_age)).filter(status="A")
    if gender!= 'A':
        singles = singles.filter(gender=gender)
    singles = singles.order_by('gender', 'last_name', 'first_name')

    template_name = 'matches/search_results_singles_list.html'
    context = {'user': request.user, 'circle': circle.name,
               'gender': request.POST['gender'], 'singles': singles,
               'form_header': 'CIRCLE', 'form_subheader': circle.name,
               'gender_display': gender_display, 'age_display': age_display}
    return render(request, template_name, context)

@login_required
def search_results_by_advocate(request, min_age, max_age, gender, gender_display, age_display):
    '''
    Produces the results and then renders the template for search results for 'singles by advocate'
    '''

    advocate = Advocate.objects.get(user_id=request.POST['singles_by_advocate'])
    singles = Single.objects.filter(created_by_id=advocate.user_id)\
                            .filter(age__range=(min_age, max_age)).filter(status="A")
    if gender!= 'A':
        singles = singles.filter(gender=gender)
    singles = singles.order_by('gender', 'last_name', 'first_name')

    template_name = 'matches/search_results_singles_list.html'
    context = {'user': request.user,
               'singles': singles,
               'form_header': 'ADVOCATE', 'form_subheader': '{} {}'.format(advocate.user.last_name, advocate.user.first_name),
               'gender_display': gender_display, 'age_display': age_display}
    return render(request, template_name, context)


def display_advocate_contact_info(request, pk):
    '''
    This form acts as a pop-up and displays the advocates basic contact info.
    User clicks on the Advocate to access this form.
     '''
    advocate = Single.objects.get(pk=pk).created_by

    template_name = 'matches/advocate_contact_info.html'
    context= {'advocate': advocate}
    return render(request, template_name, context)
