from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import CustomUserCreationForm,HobbyForm
from .models import Hobby

# Create your views here.


def dashboard(request):
    return render(request, "handleusers/dashboard.html")

def register(request):

    #if the user is authenticated, redirect them to home
    if request.user.is_authenticated:
        return redirect('/')

    #when the signup form is accessed
    if request.method=="GET":
        return render(request, "handleusers/register.html",{"form":CustomUserCreationForm})

    #when an user is trying to sign up
    elif request.method=="POST":
        #make a new form with the details filled up
        form=CustomUserCreationForm(request.POST)

        #check if all the fields given are valid for saving to database
        if form.is_valid():
            
            #checking for the already existing
            #this will get all the fields that have been filled by the user
            userDict=form.cleaned_data

            #getting the username and email entered
            username=userDict['username']
            email=userDict['email']

            #cchecking the database
            checkUser=User.objects.filter(username=username).exists()
            checkEmail=User.objects.filter(email=email).exists()

            if checkEmail or checkUser:
                msg='Looks like username or email already exists..!'
                print(msg)
                return render(reverse("dashboard"))
                
                #raise forms.ValidationError(msg)
                
            else:
                user=form.save()
            
                #make the user login
                login(request,user)
                #reverse() is used to get the URL from the url_name
                return redirect(reverse("dashboard"))

            
        return redirect(reverse("dashboard"))


def addHobby(request):

    if request.user.is_authenticated:

        if request.method=="POST":
            hobbyform=HobbyForm(data=request.POST)
            

            if hobbyform.is_valid():
                
                hobbyf=hobbyform.cleaned_data
                hobbyname=hobbyf['hobbyname']
                username=request.user
                checksave=Hobby.objects.create(user=username,hobbyname=hobbyname)

        else:
            
            context={
                'form':HobbyForm,
            }
            return render (request, 'handleusers/hobby.html',context=context)

    else:
        return render(request,'handleusers/requestlogin.html')

    return redirect(reverse('dashboard'))

def viewhobby(request):
    if request.user.is_authenticated:

        if request.method=="POST":

            hobbyid=request.POST.get('hobbyname')
            #get the instance from the hobby id
            instance=Hobby.objects.get(id=hobbyid)
            
            if instance: #on successful retrieval
                instance.delete()
                print(f"{instance} deleted...")
            else:
                print("Error")

        hobbylist=request.user.hobby_set.all()
    
        context={
            'list':hobbylist,
        }
        return render(request,'handleusers/hobbylist.html',context=context)

    else:
        return render(request,'handleusers/requestlogin.html')