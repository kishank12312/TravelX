from django.shortcuts import render
from django.http import HttpResponse
from . import Functions
import sqlite3

# Create your views here.
def booking_home(request):
    return render(request,'Booking/Booking_home.html')
def choice(request,slug):
    if slug=='Book_Ticket':
        return render(request,'Booking/Book_Ticket.html')
    if slug=='Data_submit':
        con=sqlite3.connect('Database.db')
        cur=con.cursor()
        fpost,tpost,dpost=request.POST.get('From'),request.POST.get('To'),request.POST.get('Date')
        f,t=Functions.convert_id(fpost,tpost,cur)
        train_ids=Functions.direct_search(f,t,cur)
        if train_ids==[]:
            inds=Functions.indirect_search(f,t,cur)
            if inds==[]:
                train_ids=None
        else:
            arrivals,departs,train_names,classes,rn,routes=[],[],[],[],[],[]
            for i in range(len(train_ids)):
                rn.append(i)
                routes.append(Functions.route(train_ids[i],cur))
                arr,dept=Functions.timings(train_ids[i],f,t,cur)
                arrivals.append(arr);departs.append(dept)
                name=Functions.namefinder(train_ids[i],cur);train_names.append(name)
                clses=Functions.class_finder(train_ids[i],cur);classes.append(clses)                        
        return render(request,'Booking/Search_results.html',{'input_data':[fpost,tpost,dpost],'direct':[train_names,train_ids,departs,arrivals,classes,rn,routes]})