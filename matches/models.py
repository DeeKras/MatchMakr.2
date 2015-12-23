from django.db import models
from django.contrib.auth.models import User
from django.forms.models import modelform_factory

from validators import lowest_age
from utils import GENDER_CHOICES, DEACTIVATE_SINGLES_CHOICES, SINGLE_STATUS_CHOICES

class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


class Circle(models.Model):
    name = models.CharField(max_length=50, blank=False)
    code = models.CharField(max_length=6, blank=False)
    admin = models.CharField(max_length=30, blank=False)
    admin_phone = models.CharField(max_length=15, blank=False)
    admin_email = models.EmailField()
    short_desc = models.CharField(max_length=255, blank=False)
    desc = models.CharField(max_length=1500, blank=True)
    members = models.ManyToManyField("auth.User", blank=True)

    class Meta:
        verbose_name_plural = 'circles'

    def __unicode__(self):
        return u'{}: {}'.format(self.code, self.name)


class Advocate(models.Model):
    user = models.OneToOneField(User)

    city = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=20, blank=False)
    phone = models.CharField(max_length=15, blank=True)

    circles = models.ManyToManyField("matches.Circle", blank=True)

    how_added = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = 'advocates'

    def __unicode__(self):
        return u'{}: {} : {}'.format(self.pk, self.user.username, self.user.last_name)


class AdvocateChangeLog(models.Model):
    user = models.OneToOneField(User)

    city = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=20, blank=False)
    phone = models.CharField(max_length=15, blank=False)

    circles = models.ManyToManyField("matches.Circle", blank=True)

    ip_of_change = models.CharField(max_length=200)
    changed_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'advocate_changes'

    def __unicode__(self):
        return u'Changed {}: {} : {}'.format(self.pk, self.user.username, self.user.last_name, self.changed_date)


class Single(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    age = models.IntegerField(blank=False, validators=[lowest_age])
    location = models.CharField(max_length=100, blank=True)
    short_desc = models.CharField(max_length=3000)

    how_advocate_knows = models.CharField(max_length=100)

    mother =  models.CharField(max_length=100, blank=True)
    father =  models.CharField(max_length=100, blank=True)
    parents_location =  models.CharField(max_length=100, blank=True)

    reference =  models.CharField(max_length=100, blank=True)
    prefered_matchmaker =  models.CharField(max_length=100, blank=True)

    resume = models.FileField(upload_to='resumes/', default='resumes/None/no-file.pdf')
    photo = models.ImageField(upload_to='photos/', default='photos/None/no-img.jpg')
    profile_image = models.ImageField(upload_to='profile_jpgs/', default='profile_jpgs/None/no-img.jpg')

    created_by = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=SINGLE_STATUS_CHOICES, default="A")

    class Meta:
        verbose_name_plural = 'singles'


    def __unicode__(self):
        return u'{}: {}, {}'.format(self.pk, self.last_name, self.first_name)


class SingleChangeLog(models.Model):
    single = models.ForeignKey(Single)

    status = models.CharField(max_length=1, choices=SINGLE_STATUS_CHOICES)
    deactivate_reason = models.CharField(max_length=1, choices=DEACTIVATE_SINGLES_CHOICES)
    deactivate_date = models.DateTimeField(null=True, blank=True)
    changed_by = models.ForeignKey(User)
    changed_date = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    age = models.IntegerField()
    location = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=1500)

    how_advocate_knows = models.CharField(max_length=100)

    mother =  models.CharField(max_length=100)
    father =  models.CharField(max_length=100)
    parents_location =  models.CharField(max_length=100)

    reference =  models.CharField(max_length=100)
    prefered_matchmaker =  models.CharField(max_length=100)

    photo = models.ImageField(upload_to='photos/', default='photos/None/no-img.jpg')
    profile_image = models.ImageField(upload_to='profile_jpgs/', default='profile_jpgs/None/no-img.jpg')

    class Meta:
        verbose_name_plural = 'single_changes'

    def __unicode__(self):
        return u'Changed {}: {}, {} on {}'.format(self.pk, self.last_name, self.first_name, self.changed_date)

