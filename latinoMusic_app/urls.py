from django.urls import path
from . import views
from latinoMusic_app.views import MusicListView

app_name = 'latinoMusic_app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/register/',views.register,name='register'),
    path('accounts/login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name='logout'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('masterKumbiaPacks/',MusicListView.as_view(),name='application_details'),
    path('subscribe/',views.subscription,name='subscription'),
    path('process_subscription/',views.process_subscription,name='process_subscription'),
    path('process-payment/',views.process_payment,name='process_payment'),
    path('payment-done/',views.payment_done,name='payment_done'),
    path('payment-cancelled/',views.payment_cancelled,name='payment_cancelled'),
    path('playmusic/',views.play_Music,name='play_music'),
    path('downloadmusic/',views.download_Music,name='download_music'),
    path('email-subscription/',views.EmailSubscriptions,name='email_subscription'),
    path('latinoMusic-admin/',views.LatinoAdminSiteView.as_view(),name='latino-admin'),
    path('all-songs/',views.LatinoAdminAllSongsView.as_view(),name='latino-admin-all_songs'),
    path('all-genres/',views.LatinoAdminAllGenresView.as_view(),name='latino-admin-all_genres'),
    path('add-new_song/',views.CreateSong.as_view(),name='add-song'),
    path('add-new_genre/',views.CreateGenre.as_view(),name='add-genre'),
    path('user-profile/',views.profile,name='user-profile'),
    path('update-user/',views.UpdateProfileDetails,name='updateProfile-details'),
]


    