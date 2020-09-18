from django.contrib import admin
from video_app.models import Video, UserProfile, Ticket

# Register your models here.
admin.site.register(Video)
admin.site.register(UserProfile)
admin.site.register(Ticket)