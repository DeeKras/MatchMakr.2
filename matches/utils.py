from django.shortcuts import get_object_or_404
from django.db.models import Max
import requests
from datetime import date
import weasyprint
from PIL import Image


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

SINGLE_STATUS_CHOICES = (
    ('A', "Active"),
    ('I', 'Inactive')
)

DEACTIVATE_SINGLES_CHOICES = (
    ('E', 'Engaged or Married'),
    ('N', 'I no longer want to represent him/ her'),
    ('R', 'Single asked me to deactivate'),
    ('O', 'Other'),
)

def get_ip(request):
    ip = request.remote_addr
    if ip == '127.0.0.1':
        ip = requests.get("http://icanhazip.com/").content
    return ip

def get_today_date():
    '''
    gets today's date and formats as YYYY_MM_DD
    '''
    today = date.today()
    return '{}_{}_{}'.format(today.year, today.month, today.day)

def get_name_date(pk):
    '''
    combines Single name and today's date.
    used for naming the profile jpg
    '''
    from .models import Single
    single = get_object_or_404(Single, pk=pk)
    return '{}_{}_{}'.format(single.last_name, single.first_name, get_today_date())

def get_lastupdate_date(pk):
    '''
    gets the date of the most recent entry in the SingleChangeLog (to put as 'updated on [date]'
    '''
    from .models import SingleChangeLog
    s = SingleChangeLog.objects.filter(single_id=pk).aggregate(Max('changed_date'))['changed_date__max']
    return s.strftime("%B %d, %Y")

# create profile jpg

def create_profile_image(pk):
    '''
    all the steps of creating the profile jpg
    '''
    from .models import Single

    single = Single.objects.get(pk=pk)
    photo = create_profile_photo(single)
    html = create_profile_html(single, pk)
    profile_text_png = create_profile_text_png(html)
    save_to = create_profile_canvas(profile_text_png, photo,pk)
    return save_to

def create_profile_photo(single):
    '''
    create the photo as jpg
    '''
    if single.photo != 'photos/None/no-img.jpg':
        photo = Image.open('{}/{}'.format('media', single.photo))
    else:
        photo = Image.open('matches/static/images/NoImageAvailable.jpg')

    if photo.width < photo.height:
        baseheight = 400
        hpercent = (baseheight/float(photo.size[1]))
        wsize = int((float(photo.size[0])*float(hpercent)))
        photo = photo.resize((wsize, baseheight), Image.ANTIALIAS)
    else:
        basewidth = 500
        wpercent = (basewidth/float(photo.size[0]))
        hsize = int((float(photo.size[1])*float(wpercent)))
        photo = photo.resize((basewidth,hsize), Image.ANTIALIAS)
    photo.save('media/temp/profile_photo.jpg', 'JPEG', quality=80)
    return photo

def create_profile_html(single, pk):
    '''
    using the Single's info, create the html (which will them be saved as png to be joined with the photo)
    '''
    reference ='{}'.format(single.reference) if single.reference else 'None provided'
    matchmaker = '{}'.format(single.prefered_matchmaker) if single.prefered_matchmaker else 'None provided'
    location = '{}'.format(single.location) if single.location else 'Not provided'
    if single.mother and single.father:
        parents = '{} & {}'.format(single.father, single.mother)
    elif single.father:
        parents = '{}'.format(single.father)
    elif single.mother:
        parents = '{}'.format(single.mother)
    else:
        parents = 'Not provided'
    if parents != 'Not provided' and single.parents_location:
        parents = '{} ({})'.format(parents, single.parents_location)

    html = '<body>'
    html += '<span style="font-family: Ubuntu; font-size: 40px">'+ '{} {}'.format(single.first_name, single.last_name) + '</span><br><br>'
    html += '<b> Current location: </b>' + location +'<br><br>'
    html += '<b> Age: </b> '+ str(single.age) + '<br><br><br><br><br><br><br><br><br><br><br><br><br>'
    html += '{}'.format(single.short_desc) + '</span><br><br>'
    html += '<b> Parents: </b>' + parents +'<hr>'
    html += '<b> Reference(s): </b> ' + reference + '<br><br>'
    html += '<b> Prefered Matchmaker(s): </b> ' + matchmaker + '<br>'
    html += '<hr> <i><b> Added By: </b></i>' + '{} {} ({})'.format(single.created_by.first_name, single.created_by.last_name, single.how_advocate_knows)+ '<br>'
    html += '<i><b> Updated: </b></i>'+ get_lastupdate_date(pk)
    html += '</body>'
    return html

def create_profile_text_png(html):
    '''
    convert the html to a png
    '''
    profile_text = weasyprint.HTML(string=html)
    profile_text.write_png('media/temp/profile_text.png')
    return Image.open('media/temp/profile_text.png')

def create_profile_canvas(profile_text_png, photo, pk):
    '''
    creates a blank canvas
    then saves the profile text png  on a white background as a jpg. and saves it on the blank canvas
    then pastes the photo to the canvas
    and saves it all as a jpg
    '''
    canvas = Image.new("RGBA", (1000, 1200), 'white')

    background = Image.new("RGB", profile_text_png.size, (255, 255, 255))
    background.paste(profile_text_png, mask=profile_text_png.split()[3])
    background.save('media/temp/profile_text.jpg', 'JPEG', quality=80)

    profile_text_png = Image.open('media/temp/profile_text.jpg')
    canvas.paste(profile_text_png, (35,50))
    canvas.paste(photo, (500,50))

    save_to = 'profile_{}.jpg'.format(get_name_date(pk))
    canvas.save('media/profile_jpgs/'+save_to)
    return save_to
