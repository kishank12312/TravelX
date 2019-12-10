from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from accounts.forms import RegistrationForm,LoginForm
from . import functions
from Booking.models import Pnr,Passengers


def registration_view(request):                 #View to register new users i.e signing up
    context = {}
    if request.POST:
        #request.POST['date_of_birth'] = functions.dateify(request.POST.get('date_of_birth'))
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()                #This is done using django's bult-in authentication
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

def logout_view(request):               #view to logout
    logout(request)
    return redirect('home')


def login_view(request):                #view to login
    context = {}

    user = request.user                 #Again, this is done using django's built-in login
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
                if 'next' in request.POST:                  #If redirecting is required
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('home')

    else:
        form = LoginForm()
    
    context['login_form'] = form
    return render(request,'accounts/login.html',context)

def info_view(request):                 #View to see past bookings
    pnrs = Pnr.objects.filter(user_name=request.user.username)      #Retreiving all pnr objects with current logged in user
    names = {}
    for i in pnrs:
        names[i.booking_number]=Passengers.objects.get(passenger_id=i.passenger_id).passenger_name  #Retreiving passenger details
    return render(request,'accounts/info.html',{'pnrs':pnrs,'passengers':names})    #Sending to the html page

def ticket_view(request):           #View to see the ticket
    pnrno = request.POST.get('pnrno')               #Getting the PNR number and the passenger id
    pid = int(request.POST.get( 'passengerid'))     #Getting the PNR number and the passenger id

    pnr = Pnr.objects.get(pnr_number=pnrno,passenger_id=pid)  #Retreiving PNR object with given pnr number and passenger id
    passenger = Passengers.objects.get(passenger_id=pid)      #Retreiving passenger object with given passenger id
    return render(request,'accounts/ticket.html',{'data':request.POST,'pnr':pnr,'p':passenger}) 


def cancel_ticket(request):         #View to cancel tickets
    pnrno = request.POST.get('pnrno')           #Getting the PNR number and the passenger id
    pid = int(request.POST.get( 'passengerid')) #Getting the PNR number and the passenger id

    pnr = Pnr.objects.get(pnr_number=pnrno,passenger_id=pid)  #Retreiving PNR object with given pnr number and passenger id
    passenger = Passengers.objects.get(passenger_id=pid)
    pnr.status = 'Cancelled'                    #Setting the status='Cancelled'
    pnr.save(force_update=True )
    return render(request,'accounts/cancel.html',{'data':request.POST,'pnr':pnr,'p':passenger.passenger_name})