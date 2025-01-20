from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
import io
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage

from .forms import *
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
from django.db.models import Q
import datetime
import os
from django.shortcuts import render, redirect
from participants.forms import PaymentForm
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.conf import settings
import io
from django.conf import settings
# Create your views here
from Auth_app.models import *
from .models import *    

def sponserevents(request, id):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            event = Events.objects.get(id=id)
            user = Register.objects.get(id=request.user.id)
            number = str(event.id) + str(user.id)
            # Generate the image
            image = Image.new('RGB', (600, 400), color=(255, 255, 255))  # Light yellow background
            draw = ImageDraw.Draw(image)
            # Load a TTF font
            font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
            font = ImageFont.truetype(font_path, 24)  # Font size 24
            # Draw text with different colors
            draw.text((170, 10),f'JMC THRISSUR' , font=font, fill=(0,0,0))  # Blue text
            draw.text((150, 60), f'Sponser Name: {user.username}', font=font, fill=(0,0,0))  # Pink text
            draw.text((150, 110), f'Event Name: {event.title}', font=font, fill=(0,0,0))  # Green text
            draw.text((150, 160), f'Sponser Amount: {event.TotalCost} Rs', font=font, fill=(0,0,0))  # Green text

            # Save the image to an in-memory file
            img_io = io.BytesIO()
            image.save(img_io, 'PNG')
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
            event.sponserid=user
            event.spostatus=1
            event.save()
            sponserevent.objects.create(
                evnt_id=event,
                card=card_image,
                user_id=user
            )
            subject = 'Sponsered SuccessFully'
            message = 'you have sponsored for the '+str(event.title)+' on '+str(event.sdate)
            from_email =  'It Rendation <arjunsethumadhavan123@gmail.com>'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            email = EmailMessage(subject, message,from_email=from_email,to=recipient_list)
            email.send()
            return redirect('/')
    else:
        uni=sponserevent.objects.filter(evnt_id=id).first()
        if uni:
            messages.success(request, f'Event Is Already Sponserd', extra_tags='user_reg')
            return redirect('/view_events')
        form = PaymentForm()
        evt = Events.objects.get(id=id)
        return render(request, 'feedback.html', {'form': form, 'title': 'Sponser Event', 'amount': evt.TotalCost})



def mysponserships(request):
    if request.user.usertype == 3:
        fb=sponserevent.objects.filter(user_id=request.user.id)
        dec=sponserdecorations.objects.filter(user_id=request.user.id)
        return render(request,'viewsponserships.html',{'data':fb,'data1':dec})
    elif request.user.usertype == 1:
        fb=sponserevent.objects.all()
        dec=sponserdecorations.objects.all()
        return render(request,'view_admin.html',{'data':fb,'data1':dec})



  
def sponserdec(request, id):
    dec = decorations.objects.get(id=id)
    user = Register.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        photoform=photoForm(request.POST, request.FILES)
        if form.is_valid() and photoform.is_valid():
            image = Image.new('RGB', (600, 400), color=(255, 255, 255))  # Light yellow background
            draw = ImageDraw.Draw(image)
            # Load a TTF font
            font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
            font = ImageFont.truetype(font_path, 24)  # Font size 24
            # Draw text with different colors
            draw.text((170, 10), f'JMC THRISSUR', font=font, fill=(0,0,0))  # Blue text
            draw.text((150, 60), f'Sponser Name: {request.user.username}', font=font, fill=(0,0,0))  # Blue text
            draw.text((150, 110), f'Sponser Amount: {dec.amount} Rs', font=font, fill=(0,0,0))  # Green text
            draw.text((150, 160), f'Decoration:{dec.title}', font=font, fill=(0,0,0))  # Green text

            # Save the image to an in-memory file
            img_io = io.BytesIO()
            image.save(img_io, 'PNG')
            img_io.seek(0)
            # Define the file path within the media folder
            file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{dec.id}_{request.user.id}.png')
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # Save the image to the file system
            with open(file_path, 'wb') as f:
                f.write(img_io.getvalue())
            # Create a Django file-like object for the ImageField
            with open(file_path, 'rb') as f:
                card_image = ContentFile(f.read(), name=f'cards/card_{dec.id}_{request.user.id}.png')
            sponserdecorations.objects.create(
                decid=dec,
                user_id=user,
                card=card_image,
                adphoto=photoform.cleaned_data['adphoto']
            )
            dec.status=1
            dec.save()
            subject = 'Sponsered SuccessFully'
            message = 'you have sponsored for the '+str(dec.title)
            from_email =  'It Rendation <arjunsethumadhavan123@gmail.com>'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            email = EmailMessage(subject, message,from_email=from_email,to=recipient_list)
            email.send()
            return redirect('/viewdecorations')
    else:
        uni=sponserdecorations.objects.filter(decid=id).first()
        if uni:
            messages.success(request, f'Decoration Is Already Sponserd', extra_tags='user_reg')
            return redirect('/viewdecorations')
        form = PaymentForm()
        photoform=photoForm()

        return render(request, 'sponserdec.html', {'form': form,'photoform':photoForm ,'title': 'Sponser Decorations', 'amount': dec.amount})