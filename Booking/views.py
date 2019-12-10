from django.shortcuts import render
from django.http import HttpResponse
from . import Functions
import mysql.connector
from .models import Pnr,Passengers
from datetime import date
from django.contrib.auth.decorators import login_required


fpost,dpost,tpost=None,None,None

# Create your views here.
@login_required(login_url='/login/')            #Decorator to check if user has logged in
def booking_home(request):                      #Function to return the booking-home page 
    return render(request,'Booking/Booking_home.html')
def choice(request,slug):
    if slug=='Book_Ticket':
        today = str(date.today().year)+','+str(date.today().month-1)+','+str(date.today().day)    
        return render(request,'Booking/Book_Ticket.html',{'today':today})   #Sending today's date to html page so we can limit the minimum booking date
    else:
        return HttpResponse(slug)
def Data_submit(request):       #Function to process the search and return trains
    global fpost,dpost,tpost
    con=mysql.connector.connect(host='localhost',user='root',passwd='root',database='travelxdb')
    cur=con.cursor()               #connecting to mysql database
    identifier=Functions.create_identifier()    #creating identifier(used later to fetch and store intermediate data)
    fpost,tpost,dpost=request.POST.get('From'),request.POST.get('To'),request.POST.get('Date')   #storing data submitted by user in variables
    date=Functions.date_convert(dpost)   #converting date to right format
    f,t=Functions.convert_id(fpost,tpost,cur)    #converting names to id's
    cur.execute('insert into mdata (identifier) values ("{}");'.format(identifier))   #storing intermediate data
    con.commit()
    cur.execute('update mdata set traveldate={}, fromid={},toid={} where identifier="{}";'.format(date,f,t,identifier))  #storing intermediate data
    con.commit()
    train_ids=Functions.direct_search(f,t,cur)   #Calling the main search function
    arrivals,departs,train_names,classes,rn,routes=[],[],[],[],[],[]          #empty lists that will hold the data being sent to html page
    #INDIRECT SEARCH
    #-----------------------------------------------------------------------------------------------------#
    inds=Functions.indirect_search(f,t,cur)                   #calling the indirect search function
    if inds!=[]:               #if the indirect search didn't give an empty set(meaning trains have been found)
        x=Functions.train_lister(inds)
        final=[]
        arrives,depts,rclass,tr1,tr2,j=[],[],[],[],[],[]                       #empty lists that will hold the data being sent to html page
        for i in x:
            if i[0]==i[2]:      #If train1 and train2 are same, then it is just a direct train.
                continue        # So we skip that iteration
            print(i,x)
            n1=Functions.namefinder(i[0],cur);n2=Functions.namefinder(i[2],cur)   #Converting id to names, so it can be displayed on html page
            d=Functions.timings(i[0],f,i[1],cur)[1]                #Finding arrival and departure times of the trains
            a=Functions.timings(i[2],i[1],t,cur)[0]                #Finding arrival and departure times of the trains
            tr1.append([n1,i[0]])                                  #Appending required details into variable to be sent to html page 
            j.append(i[1])                                         #Appending required details into variable to be sent to html page 
            tr2.append([n2,i[2]])                                  #Appending required details into variable to be sent to html page             
            arrives.append(str(a))                                 #Appending required details into variable to be sent to html page         
            depts.append(str(d))                                   #Appending required details into variable to be sent to html page                                     
            rclass.append(Functions.class_finder(i[0],cur))        #Getting the list of railway classes for each train so user can choose one
        final.append(tr1)                                          #Appending details to a final list     
        final.append(j)                                            #Appending details to a final list 
        final.append(tr2)                                          #Appending details to a final list     
        final.append(depts)                                        #Appending details to a final list     
        final.append(arrives)                                      #Appending details to a final list         
        final.append(rclass)                                       #Appending details to a final list         
        no=len(final[0])                                           #Appending details to a final list     
        print(tr1)
        print(final)
    else:
        final,no=[],0
    #-------------------------------------------------------------------------------------------------#
    #DIRECT SEARCH
    for i in range(len(train_ids)):             #Direct search results
        rn.append(i)
        routes.append(Functions.route(train_ids[i],cur))        
        arr,dept=Functions.timings(train_ids[i],f,t,cur)
        arrivals.append(arr);departs.append(dept)
        name=Functions.namefinder(train_ids[i],cur);train_names.append(name)
        clses=Functions.class_finder(train_ids[i],cur);classes.append(clses)
    #---------------------------------------------------------------------------------------------------#                        
    return render(request,'Booking/Search_results.html',{'input_data':[fpost,tpost,dpost],'direct':[train_names,train_ids,departs,arrivals,classes,rn,routes],'indirect':final,'indirectno':no,'identifier':identifier,'date':date})

def pricedisplay(request):              #Function to find cost based on user input and return html page
    con=mysql.connector.connect(host='localhost',user='root',passwd='root',database='travelxdb')
    cur=con.cursor()                    #Connecting to Mysql DB
    method = None
    print(request.POST)
    identifier = request.POST.get('identifier')         
    cur.execute('select fromid,toid from mdata where identifier="{}";'.format(identifier))      #Retreiving intermediate data
    res=cur.fetchall()
    print(res,'select fromid,toid from mdata where identifier="{}";'.format(identifier))        #Retreiving intermediate data
    f,t=res[0][0],res[0][1]
    if len(request.POST.get('choice')) == 1:
        method = 'Direct'
    else:
        method = 'Indirect'
    classprice = {'1A':1,'2A':0.8333,'3A':0.6666,'FC':0.5000,'CC':0.3333,'SL':0.1666}       #Relative pricing for each class:|1A-6 times|2A-5 times|3A-4 times|FC-3 times|CC-2 times|SL-1 Time|
    c=request.POST.get('Classes')
    if method == 'Direct':
        s='choi'+'ce'
        #tid = request.POST.get('choice')
        tid = request.POST.get(s)    #Getting which trains the user has chosen
        cost=Functions.price(tid,f,t,cur)           #Calling the price function to calculate price
        cost=cost * classprice.get(request.POST.get('Classes'))     #Finding the actual price after taking railway class 
        sql='update mdata set train1={},train2=NULL,j=NULL,rclass="{}" where identifier="{}";'.format(tid,request.POST.get('Classes'),identifier)       #Storing intermediate data
        cur.execute(sql)
        con.commit()
        names = [Functions.namefinder(tid,cur),tid]         #Finding train name from train id
        junc = None             #Juction station is None as it is a direct search
    else:           #It is an indirect train that the user has chosen
        tid = int(request.POST.get('choice')[0])    #Finding which train the user has chosen
        cost=Functions.price(tid,f,t,cur)           #Calculating price using price function
        cost=cost * classprice.get(request.POST.get('Classes'));cost = round(cost,2)       #Finding the actual price after taking railway class
        print(request.POST.get('choice')[2])
        sql='update mdata set train1={},train2={},j={},rclass="{}" where identifier="{}";'.format(tid,int(request.POST.get('choice')[4]),int(request.POST.get('choice')[2]),request.POST.get('Classes'),identifier)
        cur.execute(sql)
        con.commit()
        names = [Functions.namefinder(tid,cur),tid,Functions.namefinder(int(request.POST.get('choice')[4]),cur),int(request.POST.get('choice')[4])]
        junc = Functions.stationfinder(int(request.POST.get('choice')[2]),cur)
    snames = [Functions.stationfinder(f,cur),Functions.stationfinder(t,cur)]        #List containing Station names
    cost = round(cost,2)        #Rounding the cost to 2 decimal places
    date = request.POST.get('date')         #Date of journey
    return render(request,'Booking/direct-price.html',{'data':{'snames':snames,'method':method,'cost':cost,'da':request.POST.get('da').split(','),'c':request.POST.get('Classes'),'names':names,'j':junc},'date':date})
   # return render(request,'Booking/direct-price.html',{'data':[{'snames':snames,'method':method,'cost':cost,'da':request.POST.get('da').split(','),'c':request.POST.get('Classes'),'names':names,'j':junc}]})


def passengerinfo(request):             #Function to process request and return html page
    return render(request,'Booking/Passengerinfo.html',{'date':request.POST.get('date'),'DATA':eval(request.POST['data']),'d':request.POST['Classes']})

def bookingconfirm(request):            #Function that confirms booking by adding details in database
    con=mysql.connector.connect(host='localhost',user='root',passwd='root',database='travelxdb')
    cur=con.cursor()
    #Generating PNR number based on last pnr in the table
    pnrnumber = Functions.pnrgenerator(cur)
    print(pnrnumber)
    booking_number = Functions.bookingno(cur)       #Generating Booking Number based on the last one in the table
    today = str(date.today().year)+'-'+str(date.today().month)+'-'+str(date.today().day)   #Getting today's date(Date of booking)
    username = request.user.username        #Retreiving current logged in user's Username
    status = 'Active'                       #Status of booking='Active' now. If they cancel it, it updates to 'Cancelled'
    fromcity = eval(request.POST['datat'])['snames'][0]        #Retreiving the city from which passenger departs
    tocity = eval(request.POST['datat'])['snames'][1]          #Retreiving the destination city        
    typeofjourney = eval(request.POST['datat'])['method']      #Retreiving the type of journey (Direct/Indirect)                                
    date1 = request.POST.get('date')                           #Retreiving the date of travel            
    dateofjourney = date1[0:4]+'-'+date1[4:6]+'-'+date1[6:]                                     
    if typeofjourney=="Direct":
        train1=Functions.idfinder(eval(request.POST['datat'])['names'][0],cur)      #Converting Train name to id
        junction=None               #Junction station is None as it is a direct booking
        train2=None                 #2nd Train is None as it is a direct booking
        
    else:
        #print(eval(request.POST['datat']))
        train1=Functions.idfinder(eval(request.POST['datat'])['names'][0],cur)                #Retreiving the trainsid      
        junction=Functions.convert_id(eval(request.POST['datat'])['j'],'agra',cur)[0]         #Retreiving the Junction station      
        train2=Functions.idfinder(eval(request.POST['datat'])['names'][2],cur)                #Retreiving the trainsid      
    rclass = eval(request.POST['datat'])['c']                                 #retreiving the chosen railway class                                 
    departuretime = eval(request.POST['datat'])['da'][0]                      #retreiving the departure time                    
    arrivaltime = eval(request.POST['datat'])['da'][1]                        #retreiving the arrival time               
    pnrno = Functions.pnrgenerator(cur)                                       #Generating pnr number
    seatnumbers = Functions.seatnumber(eval(request.POST['passengerno']))     #Generating seat number                                     
    print(eval(request.POST['passengerno']))
    for i in range(eval(request.POST['passengerno'])):
        #Saving all the collected info in the db (Passenger's Information)
        passenger = Passengers()
        pid = Functions.pidgenerator(cur)
        passenger.passenger_id = pid+i
        passenger.gender = request.POST['gender'+str(i)]
        passenger.passenger_name = request.POST['name'+str(i)]
        passenger.age = int(request.POST['age'+str(i)])
        passenger.phone_number = int(request.POST['num'+str(i)])
        passenger.email = request.POST['email'+str(i)]
        passenger.save(force_insert=True)
        print(dateofjourney,today)

        #Saving all the collected info in the db (PNR Information)
        booking_number = Functions.bookingno(cur)
        pnr = Pnr()
        pnr.pnr_number = pnrno
        pnr.passenger_id = pid+i
        pnr.booking_number = booking_number+i
        pnr.dateofbooking = today
        pnr.user_name = username
        pnr.status = status
        pnr.fromcity = fromcity
        pnr.tocity = tocity
        pnr.typeofjourney = typeofjourney 
        pnr.dateofjourney = dateofjourney
        pnr.train1_id = train1
        pnr.junction = junction
        pnr.train2_id = train2
        pnr.rclass = rclass
        pnr.departure_time = departuretime
        pnr.arrival_time = arrivaltime
        pnr.seat_number = seatnumbers[i]
        pnr.save(force_insert=True)

    return render(request,'Booking/confirmed.html',{'data':request.POST})