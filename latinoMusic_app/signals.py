from django.db.models.signals import post_save
from django.contrib.auth.models import User
from latinoMusic_app.models import Profile
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.core.mail import EmailMessage
from datetime import datetime
from django.shortcuts import get_object_or_404


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("profile created")
    instance.profile.save()
    print("profile updated")
@receiver(valid_ipn_received)
def ipn_receiver(sender,**kwargs):
    ipn_obj = sender
    #check buy now ipn
    if ipn_obj.txn_type == 'web_accept':
        if ipn_obj.payment_status ==ST_PP_COMPLETED:
            #payment was successful
            print('great!')
            order = get_object_or_404(Order,id=ipn_obj.invoice)
            
            if order.get_total_cost()==ipn_obj.mc_gross:
                order.paid = True
                order.save()
      #check for subscription signup IPN          
    elif ipn_obj.txn_type == "subscr_signup":
        #get user id and activate the account
        id = ipn_obj.custom
        user = User.objects.get(id=id)
        user.active = True
        user.save()
        
        subject = 'Sign Up Complete'
        message ='Thanks for signing up with MasterKumbia!'
        
        email = EmailMessage(
            subject,
            message,
            'admin@latinoMusic_app.com',
            [user.email]
            
        )
        email.send()
    #check for subscription payment IPN
    elif ipn_obj.txn_type == "subscr_payment":
        #get user id and extend user subscription
        id = ipn_obj.custom
        user = User.objects.get(id=id)
        user.extend()#extends subscription
        
        subject = 'Your invoice for {} is available'.format(datetime.strftime(datetime.now(),"%b %Y")) 
        message = 'Thanks for using our service.The balance was automatically charged from your credit card.' 
        email = EmailMessage(
            subject,
            message,
            'admin@latinoMusic_app.com',
            [user.email]
            
        ) 
        email.send()
     #check for failed subscription payment IPN   
    elif ipn_obj.txn_type == "subscr_failed":
        pass 
    #check for subscription cancellation IPN
    elif ipn_obj.txn_type =="subscr_cancel":
        pass                