from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth import login,get_user_model
from django.contrib import messages
from main.models import LibraryAdmin, Student



# Create your views here.

def register(request):
    '''register students'''
    if request.method=='POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        user = get_user_model()
        check_user = user.objects.filter(email=email)
        if check_user:
            messages.error(request,'user already exists')
        elif pass1 !=pass2:
            messages.error(request,'passwords don\'t match reenter')
        elif len(pass1)< 3:
            messages.error(request,'password too short, atleast 3 characters reqired')
        else:
            stu = user.objects.create_user(email=email,password=pass1)
            Student.objects.create(user=stu)
            messages.success(request,'account created successfully')
            return HttpResponseRedirect('/accounts/login')
 
    return render(request,'accounts/register.html')


def admin_register(request):
    '''register admin user and enforce there is only one admin'''
    
    admincheck = LibraryAdmin.objects.count() < 1
    if admincheck: 
        if request.method=='POST':
            email = request.POST.get('email')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')

            if pass1 !=pass2:
                messages.error(request,'passwords don\'t match reenter')
            elif len(pass1)< 3:
                messages.error(request,'password too short, atleast 3 characters reqired')
            else:
                user = get_user_model()
                admin_user = user.objects.create_user(email=email,password=pass1)
                admin_user.is_superuser=True
                admin_user.save()
                LibraryAdmin.objects.create(user=admin_user)
                
                return HttpResponseRedirect('/accounts/login')
    else:
        messages.error(request,'admin already exists')
    return render(request,'accounts/adminRegister.html',{'check':admincheck})

