from django.contrib import admin
from .models import Admins, Channelforforced, Movie, ChannelforBot
# Register your models here.
admin.site.register(Admins)
admin.site.register(Channelforforced)
admin.site.register(ChannelforBot)
admin.site.register(Movie)