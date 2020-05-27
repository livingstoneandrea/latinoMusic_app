from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from latinoMusic_app.forms import EmailSubscriptionForm, Profile_InfoForm, SignUpForm, SubscriptionForm,UploadSongsForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from latinoMusic_app.tokens import account_activation_token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from latinoMusic_app.models import Artist, Featured, File_uploaded, Genre, PlayList, Processed_payment, Profile, Song, SongPlay, Subscribers, Testimonial, Trending
from django.http.response import JsonResponse
from django.core import serializers
from django.views.generic import (View,TemplateView,ListView,DetailView,CreateView,DeleteView)
from django.views.generic.edit import FormMixin
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
import requests
import os
import json

# Create your views here.

class IndexView(TemplateView):  
    template_name ='latinoMusic_app/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        user = self.request.user
        context["testimonials"] = Testimonial.objects.all()
        context["Artists"]= Artist.objects.all()
        
        return context

def index(request):
    return render(request,'latinoMusic_app/index.html')

def activation_sent_view(request):
    return render(request, 'latinoMusic_app/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('latinoMusic_app:subscription')
    else:
        return render(request, 'activation_invalid.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # user.profile.first_name = form.cleaned_data.get('first_name')
            # user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
        
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account.'
            message = render_to_string('latinoMusic_app/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            #return redirect('latinoMusic_app:subscription')

    else:
        form = SignUpForm()
    return render(request, 'latinoMusic_app/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # if user.is_active():
            login(request, user)
            return HttpResponseRedirect(reverse('latinoMusic_app:application_details'))
            # else:
            return HttpResponse('Account not activated')
        else:
            print("Access denied due to invalid credential")
            print("username : {} and password entered : {}".format(username, password))
            return HttpResponse("Invalid username or password combination")
    else:
        return render(request, 'latinoMusic_app/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('latinoMusic_app:index'))

def get_userPage(request):
    songs = Song.objects.all()
    
    return render(request,'latinoMusic_app/music-display_page.html')


def process_payment(request):
    user_id = request.session.get('user_id')
    subscription = 9.00;
    
    host = request.get_host()
    
    paypal_dict = {
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':'%.2f' % subscription,
        'item_name':'',
        'invoice':'',
        'currency_code':'USD',
        'notify_url':'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url':'http://{}{}'.format(host,reverse('payment_done')),
        'cancel_return':'http://{}{}'.format(host,reverse('payment_cancelled')),
        
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request,'latinoMusic_app/process_payment.html',{'form':form})

def subscription(request):
    if request.method == 'POST':
        sub_form = SubscriptionForm(request.POST)
        if sub_form.is_valid():
            request.session['subscription_plan']= request.POST.get('plans')
            return redirect('latinoMusic_app:process_subscription')
    else:
        sub_form = SubscriptionForm()
    return render(request,'latinoMusic_app/subscription_form.html',locals())
def process_subscription(request):
    subscription_plan = request.session.get('subscription_plan')
    host = request.get_host()
    
    if request.user.is_authenticated:
        current_user = request.user.id
    print("current user",current_user)
    if subscription_plan == 'premium':
        price = "20"
        billing_cycle = 1
        billing_cycle_unit ="M"
    elif subscription_plan == 'standard':
        price = "10"
        billing_cycle = 1
        billing_cycle_unit = "M"
    else:
        price = "0"
        billing_cycle = 1
        billing_cycle_unit ="M"
    paypal_dict ={
        "cmd":"_xclick-subscriptions",
        "business":settings.PAYPAL_RECEIVER_EMAIL,
        "a3":price,#monthly price
        "p3":billing_cycle,
        "t3":billing_cycle_unit,
        "src":"1",
        "sra":"1",
        "no_note":"1",
        'item_name':'Content subscription',
        'custom':current_user,
        'currency_code':'USD',
        'notify_url':'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url':'http://{}{}'.format(host,reverse('latinoMusic_app:payment_done')),
        'cancel_return':'http://{}{}'.format(host,reverse('latinoMusic_app:payment_cancelled')),
    }    
    form = PayPalPaymentsForm(initial=paypal_dict,button_type ="subscribe") 
    return render(request,'latinoMusic_app/process_subscription.html',locals())       


@csrf_exempt
def payment_done(request):
    return redirect('latinoMusic_app:application_details')

@csrf_exempt
def payment_cancelled(request):
    return render(request,'latinoMusic_app/payment_cancelled.html')

class MusicListView(LoginRequiredMixin,ListView):
    template_name = 'latinoMusic_app/music-display_page.html'
    model = Song

    def get_context_data(self, **kwargs):
        context = super(MusicListView,self).get_context_data(**kwargs)
        user = self.request.user
        context["musics"] = Song.objects.all()
        context["trucks"] = Song.objects.all()[:4]
        context["featureds"]= Featured.objects.all()[:8]
        context["trendings"]= Trending.objects.all() 
        context["genres"]= Genre.objects.all()[:8]
        context["Artists"]= Artist.objects.all()
        context["playlists"]= PlayList.objects.all()[:5]
        # context["profile_form"]= Profile_InfoForm()
        context["profile"]= Profile.objects.get(id=user.id)
        return context
    
def profile(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)
    if profile is None:
        profile_form = Profile_InfoForm()
    else:
        profile_form = Profile_InfoForm(instance=profile)
    context = {'profile_form':profile_form}
    
    return render(request,'latinoMusic_app/user-profile.html',context)    
class MusicTemplateView(LoginRequiredMixin,FormMixin,TemplateView):
    template_name = 'latinoMusic_app/music-display_page.html'
    def get_context_data(self, **kwargs):
        context = super(MusicTemplateView).get_context_data(**kwargs)
        context["musics"] = Song.objects.all()
        context["trucks"] = Song.objects.all()
        context["featured"]= Song.objects.all()[:8]
        context["trendings"]= Song.objects.all() 
        context["genres"]= Genre.objects.all()
        context["Artists"]= Artist.objects.all()
        context["playlists"]= SongPlay.objects.all()
        return context
    
    
def UpdateProfileDetails(request):
    user = User.objects.get(pk=request.user.id)
    profile = Profile.objects.get(user=user.id)
    print(user)
    if request.is_ajax or request.method == "POST":
        form = Profile_InfoForm(request.POST,instance=profile)
        if form.is_valid():
            print("form is valid")
            instance = form.save(commit=False)
            instance.refresh_from_db()
            instance.first_name = form.cleaned_data.get('first_name')
            instance.last_name = form.cleaned_data.get('last_name')
            # instance.profile_pic = request.FILES.get('profile_pic')
            instance.email = form.cleaned_data.get('email')
            instance.phone_number = form.cleaned_data.get('phone_number')
            instance.location = form.cleaned_data.get('location')
            instance.save()
            print("user profile updated")
            # send to client side.
            return JsonResponse({"message":"succesfully updated" }, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)        

def play_Music(request):
    
    if request.is_ajax and request.method == 'GET':
        song_id = request.GET['songid']
        print("song id",song_id,os.getcwd())
        audio_file = Song.objects.get(id=song_id)
        file_url = str(audio_file.track.url)
        file_name = file_url.split('/')[-1]
        print('file name:',file_name)
        fsock = open(r'./%s'%file_url,'rb')
        # response = HttpResponse(fsock,content_type='audio/mpeg')
        # response.write(fsock.read())
        # response['track_title']=audio_file.title
       
        # response['Content-Length']= os.path.getsize(file_name)
        # fsock.close()
        return JsonResponse({'data':audio_file.title}, status=200)
    
    
def download_Music(request):
    current_site = get_current_site(request)
    print("host",current_site)
    songid = ''
    audio_link = 'http://127.0.0.1:8000'
    if request.is_ajax and request.method == "GET":
        songid = request.GET['songid'] 
        print("song id :",songid)
        audio_file = Song.objects.get(id=songid)
        r = requests.get(audio_link)
            
        music_links =[audio_link + str(audio_file.track.url)]  
        print("track link",music_links)
        for link in music_links:
            file_name = link.split('/')[-1]
            print('downloading file:%s'%file_name)
            # r = requests.get(link,stream=True)
            # with open(file_name,'wb')as f:
            #     for chunk in r.iter_content(chunk_size = 1024*1024):
            #         if chunk:
            #             f.write(chunk)
                        
            # print("%s downloaded!\n"%file_name)
            
            # send to client side.
            
            return JsonResponse({'data':file_name}, status=200)  
    else:
        return JsonResponse({'error':'exception'},status=400)
         
    
        # music_links = settings.MEDIA_URL+'audio/'+str(audio_file.track.url)
def EmailSubscriptions(request):
    
    if request.is_ajax and request.method == "POST":
        print("form is valid")
        instance = Subscribers(email=request.POST.get('email'))  
        instance.save()
        print("user subscription added")

        return JsonResponse({"message": "subscription succesful" }, status=200)
    else:
            # some form errors occured.
        return JsonResponse({"error": "Error occured"}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)    
class LatinoAdminSiteView(ListView):
    template_name ='latinoMusic_admin/latinoMusic_admin_index.html'
    model = Song
    def get_context_data(self, **kwargs):
        context = super(LatinoAdminSiteView,self).get_context_data(**kwargs)
        context["users"] = User.objects.count
        context["trucks"] = Song.objects.count
        context["subscribers"]= Subscribers.objects.count
        context["featureds"]= Song.objects.all()[:8]
        context["trendings"]= Song.objects.all() 
        context["genres"]= Genre.objects.all()[:8]
        context["Artists"]= Artist.objects.all()
        context["playlists"]= SongPlay.objects.all()
        context["profiles"]= Profile.objects.all()
        return context

class LatinoAdminAllSongsView(ListView):
    template_name ='latinoMusic_admin/all_songs.html'
    model = Song
    def get_context_data(self, **kwargs):
        context = super(LatinoAdminAllSongsView,self).get_context_data(**kwargs)
        context["trucks"] = Song.objects.all()
        context["featureds"]= Song.objects.all()[:8]
        context["trendings"]= Song.objects.all() 
        context["genres"]= Genre.objects.all()[:5]
        context["Artists"]= Artist.objects.all()
        context["profile"]= Profile.objects.all()
        
        return context

class LatinoAdminAllGenresView(ListView):
    template_name ='latinoMusic_admin/genre.html'
    model = Genre
    def get_context_data(self, **kwargs):
        context = super(LatinoAdminAllGenresView,self).get_context_data(**kwargs)
        context["genres"]= Genre.objects.all()[:5]
        context["Artists"]= Artist.objects.all()
        return context
                                
class CreateSong(CreateView):
    fields = '__all__'
    model = Song
    template_name ='latinoMusic_admin/add_song.html'
    def form_valid(self,form):
        self.object = form.save()
        self.object.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('latinoMusic_app:latino-admin-all_songs')
class DeleteSong(DeleteView):
    model = Song
    success_url = reverse_lazy('latinoMusic_admin:latino-admin-all_songs')
    
    def get_queryset(self):
        queryset =super().get_queryset()
        return queryset.filter(song_id=1)
    def delete(self,*args, **kwargs):
        messages.success(self.request,"Song Deleted")
        return super().delete(*args,**kwargs)
        
class CreateGenre(CreateView):
    fields = '__all__'
    model = Genre
    template_name ='latinoMusic_admin/addGenre.html'
    def form_valid(self,form):
        self.object = form.save()
        self.object.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('latinoMusic_app:latino-admin-all_genres')        
            
              
   