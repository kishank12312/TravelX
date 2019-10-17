from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.
def booking_home(request):
    return render(request,'Booking/Booking_home.html')
def choice(request,slug):
    if slug=='Book_Ticket':
        return render(request,'Booking/Book_Ticket.html')
    if slug=='Data_submit':
        return render(request,'Booking/return.html',{'data':request.POST})