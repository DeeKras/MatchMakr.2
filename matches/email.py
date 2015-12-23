from django.shortcuts import  render
import requests
from mysite.secret_settings import key, sandbox

from .forms import EditEmailForm

def create_html_profile_to_friend(request, single):
    sender = request.user
    email_subject = 'From {}: Profile of {}. CONFIDENTIAL!'.format(sender.username, single.last_name)
    email_body = 'I am sending you the profile of {} {}. Please do not share without express permission.  If you have any questions, you can ask me or the references in the profile.  Hey you never know where a match can come from!'.format(single.first_name, single.last_name)

    email_data= {'email_subject': email_subject,
                 'email_body': email_body,
                 'email_attachment': "media/profile_jpgs/{}".format(single.profile_image),
                 'email_from': 'dee@deekras.com',
                 'email_to': 'deekras2@gmail.com',
                 'single': single}
    return email_data

def create_html_request_resume(request, single):

    secret_url = 'http://127.0.0.1:8000/email/request_resume/47'  #TODO: need to change this to the right url

    sender = request.user
    email_subject = "From {}: I'm requesting {} {}'s resume".format(sender.username, single.first_name, single.last_name)
    email_body = "{} {}'s profile looks interesting for someone I know. I am requesting to see the full resume that is on file.".format(single.first_name, single.last_name)
    email_body += "Click here to accept " +secret_url+ "'"
    email_data= {'email_subject': email_subject,
                 'email_body': email_body,
                 'email_from': 'dee@deekras.com',
                 'email_to': 'deekras2@gmail.com',
                 'single': single,
                 'email_attachment': 'None'}
    return email_data


def edit_email(request, email_data):
    template_name = 'matches/edit_email_form.html'

    form = EditEmailForm(initial={'email_to': email_data['email_to'],
                                  'email_from': 'dee@deekras.com',
                                  'email_subject': email_data['email_subject'],
                                  'email_body': email_data['email_body'],
                                  'email_attachment': email_data['email_attachment'],
                                  'single_id': email_data['single'].id})
    context = {'form': form}
    return render(request, template_name, context)

def process_email(email_data):
    request_url = 'https://api.mailgun.net/v2/{0}/messages'.format(sandbox)
    email_attachment = email_data['attachment']
    if email_attachment == 'None':
        request = requests.post(request_url,
                            auth=('api', key),
                            data=email_data)
    else:
        request = requests.post(request_url,
                                auth=('api', key),
                                data=email_data,
                                files=[("attachment", open(email_attachment))])
    return email_data
