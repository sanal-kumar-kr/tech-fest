from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .forms import *
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
from django.db.models import Q
import datetime

from django.conf import settings
from sponser.models import *
from datetime import date 

# Create your views here.
def index(request):
    if request.user:
        todays_date = date.today() 
        data=sponserdecorations.objects.filter(decid__year=todays_date.year)
        return render(request,'index.html',{'data':data})
    else:
        todays_date = date.today() 
        data=sponserdecorations.objects.filter(decid__year=todays_date.year)
        return render(request,'index.html',{'data':data,'Isloggedin':False})


def doLogin(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        print(user)

        if user is None:
            messages.success(request, f'Invalid User !!!!!!', extra_tags='user_reg')
            return redirect('/Login')
        elif user.status == 1:
            try:
                data = Register.objects.get(username=username)
                if user.is_superuser:
                    data.usertype=1
                    data.save()
                request.session['ut'] = data.usertype
                request.session['userid'] = data.id
             
    
                login(request, user)
                messages.success(request, f'Login SuccessFull continue Your Journey '+data.username, extra_tags='user_reg')
                return redirect('/')
            except ObjectDoesNotExist:
                # Handle the case where no matching record is found
                return render(request, 'form.html', {'form': form, 'k': True})
    
        elif user.status == 0:
            messages.success(request, f'Need admins approval to login', extra_tags='user_reg')
            return redirect('/')



    else:
        form = LoginForm()
        return render(request, 'form.html', {'form': form})
def add_user(request,ut):
    if ut==10:
       return render(request,'Register.html')

        
   
    if request.method=='POST':
        print(ut)
        if ut==0:
            print(ut)
            form = StudentRegisterForm(request.POST,request.FILES)
        elif ut==2:
            form = StaffRegisterForm(request.POST,request.FILES)
        elif ut==3:
            form = SponserRegisterForm(request.POST,request.FILES)    
        try:
            Register.objects.get(username=request.POST['username'])
            messages.success(request, f'Username Already Taken', extra_tags='user_reg')
            referring_url = request.META.get('HTTP_REFERER')
            return redirect(referring_url or '/')

        except Register.DoesNotExist:
            print(form.errors)
            if form.is_valid():
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                if ut==0:
                    Register.objects.create_user(
                        username = form.cleaned_data["username"],
                        email = form.cleaned_data["email"],
                        contact = form.cleaned_data["contact"],
                        password = form.cleaned_data["password"],
                        admissionnum = form.cleaned_data["admissionnum"],
                        idproof = form.cleaned_data["idproof"],
                        department = form.cleaned_data["department"],
                        cource = form.cleaned_data["cource"],
                        status=1,
                        usertype = 0
                    )
                elif ut==2:
                    Register.objects.create_user(
                        username = form.cleaned_data["username"],
                        email = form.cleaned_data["email"],
                        password = form.cleaned_data["password"],
                        contact = form.cleaned_data["contact"],
                        idproof = form.cleaned_data["idproof"],
                        cource = form.cleaned_data["cource"],
                        status=0,
                        usertype =2
                    )
                elif ut==3:
                    Register.objects.create_user(
                        username = form.cleaned_data["username"],
                        email = form.cleaned_data["email"],
                        password = form.cleaned_data["password"],
                        contact = form.cleaned_data["contact"],
                        firm_name = form.cleaned_data["firm_name"],
                        pin = form.cleaned_data["pin"],
                        street = form.cleaned_data["street"],
                        city = form.cleaned_data["city"],
                        idproof = form.cleaned_data["idproof"],
                        firm_type = form.cleaned_data["firm_type"],
                        status=1,
                        usertype =3
                    )    

                # subject = 'You Are Registered Successfully By Staff'
                # message = "your password is " + str(password) + " your department is "
                # email_from = settings.EMAIL_HOST_USER
                # recepient_list = [email]  
                # send_mail(subject,message,email_from,recepient_list)
                return redirect('/Login')
    else:
        if ut==0:  
            print("simple",ut)
            form = StudentRegisterForm()
        elif ut==2:
            form = StaffRegisterForm()
        elif ut==3:
            form = SponserRegisterForm()    
    return render(request,'Register.html',{'form':form,'ut':ut})



def doLogout(request):
    auth.logout(request)
    return redirect('/')

def about(request):
    return render(request,'about.html')


