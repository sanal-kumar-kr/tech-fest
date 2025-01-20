from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
import io
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage

from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
from django.db.models import Q
import datetime
import os
from django.shortcuts import render, redirect
from .forms import PaymentForm
from .models import Registevevnts, Events, Register
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.conf import settings
import io
from django.conf import settings

from Admin_app.models import *
def addfeedback(request):
    if request.method=='POST':
            form = Feedbackform(request.POST,request.FILES) 
            print(form.errors)   
            if form.is_valid():
                data=form.save(commit=False)
                data.user_id=Register.objects.get(id=request.user.id)
                data.save()

                return redirect('/viewfeedback')
    else:
            form = Feedbackform()    
            return render(request,'feedback.html',{'form':form,'title':'Add Feedback'})


def addmembers(request,id):
    if request.method=='POST':
            form = groupform(request.POST,request.FILES) 
            print(form.errors)   
            if form.is_valid():
                data=form.save(commit=False)
                data.user_id=Register.objects.get(id=request.user.id)
                data.evnt_id=Events.objects.get(id=id)
                data.save()
                return redirect('/')
    else:
            form = groupform()    
            return render(request,'addmemebers.html',{'form':form})

def view_members(request,id):
        data=group.objects.filter(user_id=request.user.id,evnt_id=id)
        return render(request,'view_members.html',{'data':data})

def viewfeedback(request):
        fb=feedback.objects.all()
        return render(request,'viewfeedback.html',{'data':fb})


def Registerevent(request, id):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        gpform = groupform(request.POST,request.FILES) 
        print(form.errors)
        if gpform.is_valid():
             
            data=gpform.save(commit=False)
            data.user_id=Register.objects.get(id=request.user.id)
            data.evnt_id=Events.objects.get(id=id)
            data.save()
        if form.is_valid():
            event = Events.objects.get(id=id)
            user = Register.objects.get(id=request.user.id)
            number = str(event.id) + str(user.id)
            # Generate the image
            # Generate the image
            # image = Image.new('RGB', (800, 400), color=(255,255,255))  # Light yellow background
            # draw = ImageDraw.Draw(image)
            background_path = os.path.join(settings.BASE_DIR, 'tech1.png')
            background_image = Image.open(background_path)

            # Resize the background image if necessary to fit the desired size (800x400)
            background_image = background_image.resize((800, 400))
            draw = ImageDraw.Draw(background_image)
            # Load a TTF font
            font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
            font = ImageFont.truetype(font_path, 24)  # Font size 24
            font_x_large = ImageFont.truetype("arial.ttf", 80)
            font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
            font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
            font_small = ImageFont.truetype("arial.ttf", 18) 
            # Draw text with different colors
            draw.text((300, 90), f'IT RENDITION', font=font, fill=(0, 102, 204))  # Blue text
            draw.text((290,120), f'JMC THRISSUR', font=font, fill=(0, 102, 204))  # Blue text
            draw.text((120, 170), f'Username: {user.username}', font=font, fill=(0, 102, 204))  # Blue text
            draw.text((120, 220), f'Event Name: {event.title}', font=font, fill=(0, 102, 204))  # Pink text
            draw.text((450, 190), f'{number}', font=font_x_large, fill=(0, 102, 204))  # Green text
            # Save the image to an in-memory file
            img_io = io.BytesIO()
            background_image.save(img_io, 'PNG')
            img_io.seek(0)
            # Define the file path within the media folder
            file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{event.id}_{user.id}.png')
             # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save the image to the file system
            with open(file_path, 'wb') as f:
                f.write(img_io.getvalue())

            # Create a Django file-like object for the ImageField
            with open(file_path, 'rb') as f:
                card_image = ContentFile(f.read(), name=f'cards/card_{event.id}_{user.id}.png')


            # Create the registration event
            Registevevnts.objects.create(
                evnt_id=event,
                card=card_image,
                user_id=user
            )
          
            return redirect('/')
    else:
        uni=Registevevnts.objects.filter(user_id=request.user.id,evnt_id=id).first()
        if uni:
            messages.success(request, f'Event Is Already Registered By you', extra_tags='user_reg')
            return redirect('/view_events')
        form = PaymentForm()
        gpform = groupform()    

        evt = Events.objects.get(id=id)

        starttime=evt.stime

        paralellevent=Registevevnts.objects.filter(evnt_id__stime=starttime,user_id=request.user.id).first()
        if paralellevent:
            messages.success(request, f'Cannot register for two events occuring at same time', extra_tags='user_reg')
            return redirect('/view_events')

        if evt.event_type == "group":
            return render(request, 'payment_interface.html', {'form': form,'gpform':gpform,'title': 'Register Event', 'amount': evt.Fees})
        else:
            return render(request, 'payment_interface.html', {'form': form,'title': 'Register Event', 'amount': evt.Fees})



def myregistrations(request):
        fb=Registevevnts.objects.filter(user_id=request.user.id)
        return render(request,'viewregistration.html',{'data':fb})


def viewcertificates(request):
        fb=certificatese.objects.filter(user_id=request.user.id)
        return render(request,'viewcerti.html',{'data':fb})

def cancelevent(request,id):
    events=Registevevnts.objects.get(id=id)
    events.delete()
        # subject = 'Refund'
        # message = 'your money will be refunded within 3 days'
        # from_email =  'It Rendation <arjunsethumadhavan123@gmail.com>'
        # recipient_list = [request.user.email]
        # send_mail(subject, message, from_email, recipient_list)
        # email = EmailMessage(subject, message,from_email=from_email,to=recipient_list)
        # email.send()
    # messages.success(request, f'Event registration cancelled', extra_tags='user_reg')

    return redirect('/view_events')


def deletemyaccount(request):
    data=Register.objects.get(id=request.user.id)    
    data.delete()  
    request.session.flush()
    auth.logout(request) 
    messages.success(request, f'Account Deleted Succesfully !', extra_tags='user_reg')
    return redirect('/')