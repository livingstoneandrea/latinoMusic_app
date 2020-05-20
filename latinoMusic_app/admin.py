from django.contrib import admin
from latinoMusic_app.models import (Profile,Genre,Song,SongPlay,Artist,Processed_payment,File_uploaded)

# Register your models here.
admin.site.register(Profile)
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(SongPlay)
admin.site.register(Processed_payment)
admin.site.register(File_uploaded)

