from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
import io
from django.contrib import messages
from datetime import date,timedelta
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
from django.db.models import Q
import datetime
import os
from django.shortcuts import render, redirect
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from django.conf import settings
import io
from django.conf import settings
from participants.models import *
from datetime import date 

# Create your views here.
def view_users(request, ut):
        if ut==0:   
            data = Register.objects.filter(usertype=0,status__in=[1,2])
        elif ut == 2:
            data = Register.objects.filter(usertype=2,status__in=[1,2])
        elif ut == 3:
            data = Register.objects.filter(usertype=3,status__in=[1,2])
        print(data)
        return render(request, 'view_users.html', {'userdata': data,'ut':ut})

def users(request):
    return render(request, 'view_users.html')
def usersreq(request):
        data = Register.objects.filter(usertype=2,status=0)
        print(data)
        return render(request, 'view_usersrq.html', {'userdata': data})
def approve_user(request, id):
        user=Register.objects.get(id=id)
        user.status=1
        user.save()
        messages.success(request, f'Login SuccessFull continue Your Journey', extra_tags='user_reg')
        return redirect('/users')
def reject_user(request, id):
        user=Register.objects.get(id=id)
        user.status=3
        user.save()
        return redirect('/users')

def disable_user(request, id):
        user=Register.objects.get(id=id)
        referring_url = request.META.get('HTTP_REFERER')
        user.status=2
        user.save()
        return redirect(referring_url or '/')

def enable_user(request, id):
        user=Register.objects.get(id=id)
        referring_url = request.META.get('HTTP_REFERER')
        user.status=1
        user.save()
        return redirect(referring_url or '/')
def add_event(request):
    if request.method=='POST':
            form = addeventForm(request.POST,request.FILES) 
            print(form.errors)   
            if form.is_valid():
                data=form.save(commit=False)
                data.cod=request.user
                data.save()    
                return redirect('/view_events')
    else:
            form = addeventForm()    
            return render(request,'add_event.html',{'form':form,'title':'Add Event'})

def editevent(request,id):
    data=Events.objects.get(id=id)
    if request.method=='POST':
            form = addeventForm(request.POST,request.FILES,instance=data) 
            print(form.errors)   
            if form.is_valid():
                form.save()
                return redirect('/view_events')
    else:
            form = addeventForm(instance=data)    
            return render(request,'add_event.html',{'form':form,'title':'Edit Event'})



def addecorations(request):
    todays_date = date.today() 

    if request.method=='POST':
            form = addecorationsForm(request.POST,request.FILES) 
            if form.is_valid():
                data=form.save(commit=False)
                data.year=todays_date.year
                data.save()
                return redirect('/viewdecorations')
    else:
            form = addecorationsForm()    
            return render(request,'add_event.html',{'form':form,'title':'Add Decorations'})


def edit_dec(request,id):
    data=decorations.objects.get(id=id)
    if request.method=='POST':
            form = addecorationsForm(request.POST,request.FILES,instance=data) 
            if form.is_valid():
                form.save()
                return redirect('/viewdecorations')
    else:
            form = addecorationsForm(instance=data)    
            return render(request,'add_event.html',{'form':form,'title':'Edit Decorations'})









def delete_dec(request,id):
        data=decorations.objects.get(id=id)
        data.delete()
        return redirect('/viewdecorations')











def viewdecorations(request):
    todays_date = date.today() 
    dec=decorations.objects.filter(year=todays_date.year)
    return render(request,'view_dec.html',{'data':dec})






def View_events(request):
    currentdate=date.today()
    events=Events.objects.filter(status=1)
    for i in events:
       
        if i.sdate < currentdate:
            i.status=0
            i.save()

    return render(request,'view_events.html',{'data':events})

def registrations(request,id):
        fb=Registevevnts.objects.filter(evnt_id=id)
        return render(request,'viewregistration.html',{'data':fb})

def deleteevent(request,id):
        events=Events.objects.get(id=id)
        events.delete()
        return redirect('/view_events')

def updateprice(request,id):
    if request.method=='POST':
        events=Events.objects.get(id=id)
        if events.first and events.second and events.third:
            messages.success(request, f'Already Updated!!!!', extra_tags='user_reg')
            return redirect('/')



        events.first=Register.objects.get(id=request.POST['first'])
        events.second=Register.objects.get(id=request.POST['second'])
        events.third=Register.objects.get(id=request.POST['third'])
        events.save()
        return redirect('/')
    else:
        reg=Registevevnts.objects.filter(evnt_id=id)
        return render(request,'updateprice.html',{'data':reg})


def generatecertificates(request,id):
            evtuni=Events.objects.get(id=id)
            if not evtuni.first or not evtuni.second or not evtuni.third:
                messages.success(request, f'Please Update Prices!!!!', extra_tags='user_reg')
                return redirect('/')
            uni=certificatese.objects.filter(evnt_id=id).first()
            if uni:
                messages.success(request, f'certifiates already generated for this event', extra_tags='user_reg')
                return redirect('/')
            events=Events.objects.get(id=id)
            if events.event_type == "single":
            # Generate the image
            # image = Image.new('RGB', (800, 400), color=(255,255,255))  # Light yellow background
            # draw = ImageDraw.Draw(image)
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)

                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))

                draw = ImageDraw.Draw(background_image)
            
                
                # Load a TTF font
                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18)
                font_x_small = ImageFont.truetype("arial.ttf", 16)  
                  # Draw text with different colors
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{events.first.username}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing FIRST prize in {events.title} conducted by  Dr.John Matthai Centre ', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 
                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')

                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())

                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')

                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=events.first.id)
                )
                # sadgfdsh

                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)

                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))

                draw = ImageDraw.Draw(background_image)
            
                # Load a TTF font
            
                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18)  
                font_x_small = ImageFont.truetype("arial.ttf", 16)  
                # Draw text with different colors
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{events.second.username}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing SECOND prize in {events.title} conducted by Dr.John Matthai Centre On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

            


                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)

                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.second.id}.png')

                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())

                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.second.id}.png')

                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=events.second.id)
                )

                # hgfghjkndbsjBfjSFSJJgfjsaf
                # image = Image.new('RGB', (800, 400), color=(255, 255, 204))  # Light yellow background
                # draw = ImageDraw.Draw(image)
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)

                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))

                draw = ImageDraw.Draw(background_image)
            
                
                # Load a TTF font
                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18) 
                font_x_small = ImageFont.truetype("arial.ttf", 16)  
                # Draw text with different colors
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{events.third.username}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing THIRD prize in {events.title} conducted by Dr.John Matthai Centre On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 


            
                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)

                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.third.id}.png')

                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.third.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=events.third.id)

                )
                particip=Registevevnts.objects.filter(evnt_id=id)
                for n in particip:
                    background_path = os.path.join(settings.BASE_DIR, 'participate.png')
                    background_image = Image.open(background_path)
                    # Resize the background image if necessary to fit the desired size (800x400)
                    background_image = background_image.resize((800, 400))
                    draw = ImageDraw.Draw(background_image)
                    # Load a TTF font

                    font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                    font = ImageFont.truetype(font_path, 24)  # Font size 24
                    font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                    font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                    font_small = ImageFont.truetype("arial.ttf", 18) 
                    font_x_small = ImageFont.truetype("arial.ttf", 16)  
                    # Draw text with different colors
                    draw.text((310,145), f'This certifies that', font=font_medium, fill=(0, 0, 0))  # Pink text
                    draw.text((355,180), f'{n.user_id.username}', font=font_medium, fill=(0, 0, 0))  # Green text
                    draw.text((80,215), f'Has activily Participated in {events.title} conducted by  Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                    draw.text((80,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                    # Save the image to an in-memory file
                    # Save the image to an in-memory file
                    img_io = io.BytesIO()
                    background_image.save(img_io, 'PNG')
                    img_io.seek(0)
                    # Define the file path within the media folder
                    file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{n.user_id.username}.png')
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    # Save the image to the file system
                    with open(file_path, 'wb') as f:
                        f.write(img_io.getvalue())
                    # Create a Django file-like object for the ImageField
                    with open(file_path, 'rb') as f:
                        card_image = ContentFile(f.read(), name=f'cards/card_{n.user_id.username}.png')
                    # Create the registration event
                    certificatese.objects.create(
                        evnt_id=events,
                        card=card_image,
                        user_id=Register.objects.get(id=n.user_id.id)
                    )
            elif events.event_type == "group":
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)

                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18) 
                font_x_small = ImageFont.truetype("arial.ttf", 16) 
                f1=group.objects.filter(user_id=events.first.id,evnt_id=id).first()
                    # Draw text with different colors
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f1.user_id.username}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing FIRST prize in {events.title} conducted by Dr.John Matthai Centre On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 
                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f1.user_id.id)
                )
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)

                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18) 
                font_x_small = ImageFont.truetype("arial.ttf", 16) 
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f1.member2}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing FIRST prize in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f1.user_id.id)
                )
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)

                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18)
                font_x_small = ImageFont.truetype("arial.ttf", 16) 
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f1.member3}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing FIRST prize in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f1.user_id.id)
                )
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)

                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18) 
                font_x_small = ImageFont.truetype("arial.ttf", 16)
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f1.member4}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing FIRST prize in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f1.user_id.id)
                )


                











                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)
                # Load a TTF font
                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18)
                font_x_small = ImageFont.truetype("arial.ttf", 16) 
                f2=group.objects.filter(user_id=events.second.id,evnt_id=id).first()
                    # Draw text with different colors
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f2.user_id.username}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing SECOND prize in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f2.user_id.id)
                )
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)

                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18)
                font_x_small = ImageFont.truetype("arial.ttf", 16) 
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f2.member2}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing SECOND prize in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0))
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 
 
                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f2.user_id.id)
                )
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)

                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18)
                font_x_small = ImageFont.truetype("arial.ttf", 16) 
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f2.member3}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing SECOND prize in {events.title} conducted by Dr.John Matthai Centre On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 
                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f2.user_id.id)
                )
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)

                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18) 
                font_x_small = ImageFont.truetype("arial.ttf", 16)
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f2.member4}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing SECOND prize in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f2.user_id.id)
                )
                background_path = os.path.join(settings.BASE_DIR, 'certi.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)

                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18) 
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)
                # Load a TTF font
                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18)
                font_x_small = ImageFont.truetype("arial.ttf", 16) 
                f3=group.objects.filter(user_id=events.third.id,evnt_id=id).first()
                    # Draw text with different colors
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f3.user_id.username}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing THIRD prize in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 
                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f3.user_id.id)
                )
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)
                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18)
                font_x_small = ImageFont.truetype("arial.ttf", 16) 
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f3.member2}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing THIRD prize in {events.title} conducted by Dr.John Matthai Centrer', font=font_x_small, fill=(0, 0, 0))
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 
                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f3.user_id.id)
                )
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)
                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18)
                font_x_small = ImageFont.truetype("arial.ttf", 16) 
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f3.member3}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For Succesfully Securing THIRD prize in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f3.user_id.id)
                )
                background_path = os.path.join(settings.BASE_DIR, 'winner.png')
                background_image = Image.open(background_path)
                # Resize the background image if necessary to fit the desired size (800x400)
                background_image = background_image.resize((800, 400))
                draw = ImageDraw.Draw(background_image)

                font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                font = ImageFont.truetype(font_path, 24)  # Font size 24
                font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                font_small = ImageFont.truetype("arial.ttf", 18)
                font_x_small = ImageFont.truetype("arial.ttf", 16) 
                # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                # draw.text((300,80), f'APPRECIATION', font=font_large, fill=(0, 0, 0))  # Green text
                draw.text((160,145), f'THIS CERTIFICATE IS PROUDLY PRESENTED TO', font=font_medium, fill=(0, 0, 0))  # Pink text
                draw.text((375,180), f'{f3.member4}', font=font_medium, fill=(0, 0, 0))  # Green text
                draw.text((45,215), f'For succesfully securing THIRD prize in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                draw.text((45,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                # Save the image to an in-memory file
                img_io = io.BytesIO()
                background_image.save(img_io, 'PNG')
                img_io.seek(0)
                # Define the file path within the media folder
                file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{events.first.id}.png')
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Save the image to the file system
                with open(file_path, 'wb') as f:
                    f.write(img_io.getvalue())
                # Create a Django file-like object for the ImageField
                with open(file_path, 'rb') as f:
                    card_image = ContentFile(f.read(), name=f'cards/card_{events.first.id}.png')
                # Create the registration event
                certificatese.objects.create(
                    evnt_id=events,
                    card=card_image,
                    user_id=Register.objects.get(id=f3.user_id.id)
                )
                particip=Registevevnts.objects.filter(evnt_id=id)
                for n in particip:
                    mem=group.objects.filter(user_id=n.user_id.id).first()
                    background_path = os.path.join(settings.BASE_DIR, 'participate.png')
                    background_image = Image.open(background_path)
                    # Resize the background image if necessary to fit the desired size (800x400)
                    background_image = background_image.resize((800, 400))
                    draw = ImageDraw.Draw(background_image)
                    # Load a TTF font

                    font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                    font = ImageFont.truetype(font_path, 24)  # Font size 24
                    font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                    font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                    font_small = ImageFont.truetype("arial.ttf", 18)
                    font_x_small = ImageFont.truetype("arial.ttf", 16)  
                    # Draw text with different colors
                    # Draw text with different colors
                    # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                    # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                    # draw.text((300,80), f'PARTICIPATION', font=font_large, fill=(0, 0, 0))  # Green text
                    draw.text((310,145), f'This certifies that', font=font_medium, fill=(0, 0, 0))  # Pink text
                    draw.text((375,180), f'{mem.user_id.username}', font=font_medium, fill=(0, 0, 0))  # Green text
                    draw.text((80,215), f'Has activily Participated in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                    draw.text((80,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

    # Blue text
                    
                    # Save the image to an in-memory file
                    # Save the image to an in-memory file
                    img_io = io.BytesIO()
                    background_image.save(img_io, 'PNG')
                    img_io.seek(0)
                    # Define the file path within the media folder
                    file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{n.user_id.username}.png')
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    # Save the image to the file system
                    with open(file_path, 'wb') as f:
                        f.write(img_io.getvalue())
                    # Create a Django file-like object for the ImageField
                    with open(file_path, 'rb') as f:
                        card_image = ContentFile(f.read(), name=f'cards/card_{n.user_id.username}.png')
                    # Create the registration event
                    certificatese.objects.create(
                        evnt_id=events,
                        card=card_image,
                        user_id=Register.objects.get(id=mem.user_id.id)
                    )


                    background_path = os.path.join(settings.BASE_DIR, 'participate.png')
                    background_image = Image.open(background_path)
                    # Resize the background image if necessary to fit the desired size (800x400)
                    background_image = background_image.resize((800, 400))
                    draw = ImageDraw.Draw(background_image)
                    # Load a TTF font

                    font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                    font = ImageFont.truetype(font_path, 24)  # Font size 24
                    font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                    font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                    font_small = ImageFont.truetype("arial.ttf", 18)
                    font_x_small = ImageFont.truetype("arial.ttf", 16)  
                    # Draw text with different colors
                    # Draw text with different colors
                    # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                    # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                    # draw.text((300,80), f'PARTICIPATION', font=font_large, fill=(0, 0, 0))  # Green text
                    draw.text((310,145), f'This certifies that', font=font_medium, fill=(0, 0, 0))  # Pink text
                    draw.text((375,180), f'{mem.member2}', font=font_medium, fill=(0, 0, 0))  # Green text
                    draw.text((80,215), f'Has activily Participated in {events.title} conducted by Dr.John Matthai Centre', font=font_x_small, fill=(0, 0, 0)) 
                    draw.text((80,240), f'On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                    # draw.text((10, 10), f'CERTIFICATION', font=font, fill=(0, 102, 204))  # Blue text
                    # draw.text((10, 60), f'FOR', font=font, fill=(204, 0, 102))  # Pink text
                    # draw.text((10, 110), f'PARTICIPATION', font=font, fill=(0, 153, 0))  # Green text
                    # draw.text((10, 160), f'This is Certificate That', font=font, fill=(0, 153, 0))  # Green text
                    # draw.text((10, 220), f'{n.user_id.username}', font=font, fill=(0, 102, 204))
                    # draw.text((10, 280), f'Has Activily Participated In {events.title} conducted by Dr,John Mathai center on {events.sdate}', font=font, fill=(0, 153, 0))  # Green text
    # Blue text
                    
                    # Save the image to an in-memory file
                    # Save the image to an in-memory file
                    img_io = io.BytesIO()
                    background_image.save(img_io, 'PNG')
                    img_io.seek(0)
                    # Define the file path within the media folder
                    file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{n.user_id.username}.png')
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    # Save the image to the file system
                    with open(file_path, 'wb') as f:
                        f.write(img_io.getvalue())
                    # Create a Django file-like object for the ImageField
                    with open(file_path, 'rb') as f:
                        card_image = ContentFile(f.read(), name=f'cards/card_{n.user_id.username}.png')
                    # Create the registration event
                    certificatese.objects.create(
                        evnt_id=events,
                        card=card_image,
                        user_id=Register.objects.get(id=mem.user_id.id)
                    )


                    background_path = os.path.join(settings.BASE_DIR, 'participate.png')
                    background_image = Image.open(background_path)
                    # Resize the background image if necessary to fit the desired size (800x400)
                    background_image = background_image.resize((800, 400))
                    draw = ImageDraw.Draw(background_image)
                    # Load a TTF font

                    font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                    font = ImageFont.truetype(font_path, 24)  # Font size 24
                    font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                    font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                    font_small = ImageFont.truetype("arial.ttf", 18)
                    font_x_small = ImageFont.truetype("arial.ttf", 16)  
                    # Draw text with different colors
                    # Draw text with different colors
                    # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                    # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                    # draw.text((300,80), f'PARTICIPATION', font=font_large, fill=(0, 0, 0))  # Green text
                    draw.text((310,145), f'This certifies that', font=font_medium, fill=(0, 0, 0))  # Pink text
                    draw.text((375,180), f'{mem.member3}', font=font_medium, fill=(0, 0, 0))  # Green text
                    draw.text((80,215), f'Has activily Participated in {events.title} conducted by Dr.John Matthai Centre On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 
                    draw.text((80,240), f'Has activily Participated in {events.title} conducted by Dr.John Matthai Centre On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                    # draw.text((10, 10), f'CERTIFICATION', font=font, fill=(0, 102, 204))  # Blue text
                    # draw.text((10, 60), f'FOR', font=font, fill=(204, 0, 102))  # Pink text
                    # draw.text((10, 110), f'PARTICIPATION', font=font, fill=(0, 153, 0))  # Green text
                    # draw.text((10, 160), f'This is Certificate That', font=font, fill=(0, 153, 0))  # Green text
                    # draw.text((10, 220), f'{n.user_id.username}', font=font, fill=(0, 102, 204))
                    # draw.text((10, 280), f'Has Activily Participated In {events.title} conducted by Dr,John Mathai center on {events.sdate}', font=font, fill=(0, 153, 0))  # Green text
    # Blue text
                    
                    # Save the image to an in-memory file
                    # Save the image to an in-memory file
                    img_io = io.BytesIO()
                    background_image.save(img_io, 'PNG')
                    img_io.seek(0)
                    # Define the file path within the media folder
                    file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{n.user_id.username}.png')
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    # Save the image to the file system
                    with open(file_path, 'wb') as f:
                        f.write(img_io.getvalue())
                    # Create a Django file-like object for the ImageField
                    with open(file_path, 'rb') as f:
                        card_image = ContentFile(f.read(), name=f'cards/card_{n.user_id.username}.png')
                    # Create the registration event
                    certificatese.objects.create(
                        evnt_id=events,
                        card=card_image,
                        user_id=Register.objects.get(id=mem.user_id.id)
                    )

                    background_path = os.path.join(settings.BASE_DIR, 'participate.png')
                    background_image = Image.open(background_path)
                    # Resize the background image if necessary to fit the desired size (800x400)
                    background_image = background_image.resize((800, 400))
                    draw = ImageDraw.Draw(background_image)
                    # Load a TTF font

                    font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
                    font = ImageFont.truetype(font_path, 24)  # Font size 24
                    font_large = ImageFont.truetype("arial.ttf", 30)  # Large font size
                    font_medium = ImageFont.truetype("arial.ttf", 20)  # Medium font size
                    font_small = ImageFont.truetype("arial.ttf", 18)
                    font_x_small = ImageFont.truetype("arial.ttf", 16)  
                    # Draw text with different colors
                    # draw.text((300,10), f'CERTIFICATE', font=font_large, fill=(0, 0, 0))  # Blue text
                    # draw.text((380,50), f'OF', font=font_medium, fill=(0, 0, 0))  # Pink text
                    # draw.text((300,80), f'PARTICIPATION', font=font_large, fill=(0, 0, 0))  # Green text
                    draw.text((310,145), f'This certifies that', font=font_medium, fill=(0, 0, 0))  # Pink text
                    draw.text((375,180), f'{mem.member4}', font=font_medium, fill=(0, 0, 0))  # Green text
                    draw.text((80,215), f'Has activily Participated in {events.title} conducted by Dr.John Matthai Centre On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 
                    draw.text((80,240), f'Has activily Participated in {events.title} conducted by Dr.John Matthai Centre On {events.sdate}', font=font_x_small, fill=(0, 0, 0)) 

                    # draw.text((10, 10), f'CERTIFICATION', font=font, fill=(0, 102, 204))  # Blue text
                    # draw.text((10, 60), f'FOR', font=font, fill=(204, 0, 102))  # Pink text
                    # draw.text((10, 110), f'PARTICIPATION', font=font, fill=(0, 153, 0))  # Green text
                    # draw.text((10, 160), f'This is Certificate That', font=font, fill=(0, 153, 0))  # Green text
                    # draw.text((10, 220), f'{n.user_id.username}', font=font, fill=(0, 102, 204))
                    # draw.text((10, 280), f'Has Activily Participated In {events.title} conducted by Dr,John Mathai center on {events.sdate}', font=font, fill=(0, 153, 0))  # Green text
    # Blue text
                    
                    # Save the image to an in-memory file
                    # Save the image to an in-memory file
                    img_io = io.BytesIO()
                    background_image.save(img_io, 'PNG')
                    img_io.seek(0)
                    # Define the file path within the media folder
                    file_path = os.path.join(settings.MEDIA_ROOT, 'cards', f'card_{n.user_id.username}.png')
                    # Ensure the directory exists
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    # Save the image to the file system
                    with open(file_path, 'wb') as f:
                        f.write(img_io.getvalue())
                    # Create a Django file-like object for the ImageField
                    with open(file_path, 'rb') as f:
                        card_image = ContentFile(f.read(), name=f'cards/card_{n.user_id.username}.png')
                    # Create the registration event
                    certificatese.objects.create(
                        evnt_id=events,
                        card=card_image,
                        user_id=Register.objects.get(id=mem.user_id.id)
                    )















            # sadgfdsh






        # tyuiop

                
            return redirect('/')


