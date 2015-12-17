from django.contrib import admin

from .models import Advocate, Single, Circle, SingleChangeLog

admin.site.register(Advocate)
admin.site.register(Single)
admin.site.register(Circle)
admin.site.register(SingleChangeLog)
