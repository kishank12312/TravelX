from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from accounts.forms import RegistrationForm,LoginForm
from . import functions
from Booking.models import Pnr,Passengers


def registration_view(request):
    context = {}
    if request.POST:
        #request.POST['date_of_birth'] = functions.dateify(request.POST.get('date_of_birth'))
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email = email, password = raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    
    return render(request,'accounts/signup.html',context)

def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)

            if user:
                login(request,user)
                return redirect('home')

    else:
        form = LoginForm()
    
    context['login_form'] = form
    return render(request,'accounts/login.html',context)

def info_view(request):
    pnrs = Pnr.objects.filter(user_name=request.user.username)
    names = {}
    for i in pnrs:
        names[i.pnr_number]=Passengers.objects.get(passenger_id=i.passenger_id).passenger_name
    return render(request,'accounts/info.html',{'pnrs':pnrs,'passengers':names})

def ticket_view(request):
    pnrno = request.POST.get('pnrno')
    pid = int(request.POST.get( 'passengerid'))

    pnr = Pnr.objects.get(pnr_number=pnrno,passenger_id=pid)
    passenger = Passengers.objects.get(passenger_id=pid)
    return render(request,'accounts/ticket.html',{'data':request.POST,'pnr':pnr,'p':passenger})