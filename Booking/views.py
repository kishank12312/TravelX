from django.shortcuts import render
from django.http import HttpResponse
from . import Functions
import sqlite3


fpost,dpost,tpost=None,None,None

# Create your views here.
def booking_home(request):
    return render(request,'Booking/Booking_home.html')
def choice(request,slug):
    if slug=='Book_Ticket':
        return render(request,'Booking/Book_Ticket.html')
    else:
        return HttpResponse(slug)
def Data_submit(request):
    global fpost,dpost,tpost
    con=sqlite3.connect('Database.db')
    cur=con.cursor()
    identifier=Functions.create_identifier()
    fpost,tpost,dpost=request.POST.get('From'),request.POST.get('To'),request.POST.get('Date')
    date=Functions.date_convert(dpost)
    f,t=Functions.convert_id(fpost,tpost,cur)
    cur.execute('insert into mdata (identifier) values ("{}");'.format(identifier))
    con.commit()
    cur.execute('update mdata set traveldate={}, fromid={},toid={} where identifier="{}";'.format(date,f,t,identifier))
    con.commit()
    train_ids=Functions.direct_search(f,t,cur)
    arrivals,departs,train_names,classes,rn,routes=[],[],[],[],[],[]
    #INDIRECT SEARCH
    #-----------------------------------------------------------------------------------------------------#
    inds=Functions.indirect_search(f,t,cur)
    if inds!=[]:
        x=Functions.train_lister(inds)
        final=[]
        arrives,depts,rclass,tr1,tr2,j=[],[],[],[],[],[]
        for i in x:
            if i[0]==i[2]:
                continue
            print(i,x)
            n1=Functions.namefinder(i[0],cur);n2=Functions.namefinder(i[2],cur)
            d=Functions.timings(i[0],f,i[1],cur)[1]
            a=Functions.timings(i[2],i[1],t,cur)[0]
            tr1.append([n1,i[0]])
            j.append(i[1])
            tr2.append([n2,i[2]])
            arrives.append(str(a))
            depts.append(str(d))
            rclass.append(Functions.class_finder(i[0],cur))
        final.append(tr1)
        final.append(j)
        final.append(tr2)
        final.append(depts)
        final.append(arrives)
        final.append(rclass)
        no=len(final[0])
        print(tr1)
        print(final)
    else:
        final,no=[],0
    #-------------------------------------------------------------------------------------------------#
    #DIRECT SEARCH
    for i in range(len(train_ids)):
        rn.append(i)
        routes.append(Functions.route(train_ids[i],cur))
        arr,dept=Functions.timings(train_ids[i],f,t,cur)
        arrivals.append(arr);departs.append(dept)
        name=Functions.namefinder(train_ids[i],cur);train_names.append(name)
        clses=Functions.class_finder(train_ids[i],cur);classes.append(clses)
    #---------------------------------------------------------------------------------------------------#                        
    return render(request,'Booking/Search_results.html',{'input_data':[fpost,tpost,dpost],'direct':[train_names,train_ids,departs,arrivals,classes,rn,routes],'indirect':final,'indirectno':no,'identifier':identifier})

def pricedisplay(request):
    con=sqlite3.connect('Database.db')
    cur=con.cursor()
    method = None
    print(request.POST)
    identifier = request.POST.get('identifier')
    cur.execute('select fromid,toid from mdata where identifier="{}";'.format(identifier))
    res=cur.fetchall()
    print(res,'select fromid,toid from mdata where identifier="{}";'.format(identifier))
    f,t=res[0][0],res[0][1]
    if len(request.POST.get('choice')) == 1:
        method = 'Direct'
    else:
        method = 'Indirect'
    classprice = {'1A':1,'2A':0.8333,'3A':0.6666,'FC':0.5000,'CC':0.3333,'SL':0.1666}
    c=request.POST.get('Classes')
    if method == 'Direct':
        tid = request.POST.get('choice')
        cost=Functions.price(tid,f,t,cur)
        cost=cost * classprice.get(request.POST.get('Classes'))
        sql='update mdata set train1={},train2=NULL,j=NULL,rclass="{}" where identifier="{}";'.format(tid,request.POST.get('Classes'),identifier)
        cur.execute(sql)
        con.commit()
        names = [Functions.namefinder(tid,cur),tid]
        junc = None
    else:
        tid = int(request.POST.get('choice')[0])
        cost=Functions.price(tid,f,t,cur)
        cost=cost * classprice.get(request.POST.get('Classes'));cost = round(cost,2)
        sql='update mdata set train1={},train2={},j={},rclass="{}" where identifier="{}";'.format(tid,int(request.POST.get('choice')[4]),int(request.POST.get('choice')[2]),request.POST.get('Classes'),identifier)
        cur.execute(sql)
        con.commit()
        names = [Functions.namefinder(tid,cur),tid,Functions.namefinder(int(request.POST.get('choice')[4]),cur),int(request.POST.get('choice')[4])]
        junc = Functions.stationfinder(int(request.POST.get('choice')[2]),cur)
    snames = [Functions.stationfinder(f,cur),Functions.stationfinder(t,cur)]
    cost = round(cost,2)
    return render(request,'Booking/direct-price.html',{'data':{'snames':snames,'method':method,'cost':cost,'da':request.POST.get('da').split(','),'c':request.POST.get('Classes'),'names':names,'j':junc}})


def passengerinfo(request):
    return render(request,'Booking/Passengerinfo.html')