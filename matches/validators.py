from django.core.exceptions import ValidationError

def lowest_age(age):
    if age < 18:
        raise ValidationError('%s is too young for this project' % age)