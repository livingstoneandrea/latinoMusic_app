from django.contrib import admin
from latinoMusic_app.models import Artist, Featured, File_uploaded, Genre, PlayList, Processed_payment, Profile, Song, SongPlay, Subscribers, Testimonial, Trending

# Register your models here.
admin.site.register(Profile)
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(SongPlay)
admin.site.register(Processed_payment)
admin.site.register(File_uploaded)
admin.site.register(Trending)
admin.site.register(Featured)
admin.site.register(PlayList)
admin.site.register(Subscribers)
admin.site.register(Testimonial)

