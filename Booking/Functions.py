#import mysql.connector
#con=mysql.connector.connect(host='localhost',user='root',passwd='root',database='travelxdb')
#cur=con.cursor()

def route(train_id,cur):
    '''Returns tuple of strings as (origin,end_point)'''
    sql='select origin,end_point from trains where train_id={};'.format(train_id)
    cur.execute(sql);res=cur.fetchall()
    o,e=res[0][0],res[0][1]
    return o,e

def class_finder(train_id,cur):
    '''Returns list of classes (list of strings like ['2S', 'SL', '3A', '2A', '1A'])'''
    sql='select railway_classes from trains where train_id={};'.format(train_id)
    cur.execute(sql)
    res=cur.fetchall()
    res=res[0][0]
    classes=res.split(',')
    return classes
#print(class_finder(7,cur))
def namefinder(train_id,cur):
    '''Takes int(train id) and returns the train name as str'''
    sql='select train_name from trains where train_id={};'.format(train_id)
    cur.execute(sql)
    res=cur.fetchall()
    train_name=res[0][0]
    return train_name

def idfinder(train_name,cur):
    '''Takes int(train id) and returns the train name as str'''
    sql='select train_id from trains where train_name="{}";'.format(train_name)
    cur.execute(sql)
    res=cur.fetchall()
    train_id=res[0][0]
    return train_id

def timings(train_id,f,t,cur):
    '''Returns tuple of strings as (arrival,departure)'''
    sql1='select departure_time from routes where train_id={} and station_id={};'
    print(sql1.format(train_id,f),train_id,f)
    cur.execute(sql1.format(train_id,f))
    res=cur.fetchall()
    depart=str(res[0][0]);print(depart)
    if depart=='None':
        sql2='select arrival_time from routes where train_id={} and station_id={};'
        cur.execute(sql2.format(train_id,f))
        res=cur.fetchall()
        depart=str(res[0][0])
    sql2='select arrival_time from routes where train_id={} and station_id={};'
    print(sql2.format(train_id,t),train_id,t)
    cur.execute(sql2.format(train_id,t))
    res=cur.fetchall();print(res)
    arrive=str(res[0][0]);print(arrive)
    return arrive,depart 
#print(timings(7,1,6,cur))

def date_convert(date):
    '''Returns date formatted as yyyymmdd, str'''
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_nos=['01','02','03','04','05','06','07','08','09','10','11','12']
    i=months.index(date[:3]);month=month_nos[i]
    comma=date.find(',')
    day=date[4:comma]
    year=date[len(date)-4:len(date)]
    date_formatted=int(str(year)+str(month)+str(day))
    return date_formatted

def convert_id(ft,tt,cur):
    '''Returns tuple of train id's(ints) as (from,to)'''
    text='select station_id from stations where station_name="{}";'
    names,ids=[ft,tt],[]
    for i in range(2):
        cur.execute(text.format(names[i]))
        res=cur.fetchall()
        res=res[0][0]
        ids.append(res)
    return (ids[0],ids[1])
#print(convert_id('agra','new delhi',cur)) 

def direct_search(f,t,cur):
    '''Returns list of train_ids(ints) of direct trains'''
    sql='''select train_id from routes 
    where station_id={} or station_id={}
    group by train_id having count(train_id)>1;'''.format(f,t)
    cur.execute(sql)
    res=cur.fetchall()
    train_ids=[]
    #print(res)
    for i in res:
        train_ids.append(i[0])
    return train_ids

def indirect_search(f,t,cur):
    '''Returns [list of train_ids(ints) till junction,train_id of junction itself,list of train_ids(ints) from junction to destination]'''
    junctions=[5,1,7,6,13]
    final=[]
    for i in junctions:
        train1=direct_search(f,i,cur)
        if train1!=[]:
            train2=direct_search(i,t,cur)
            if train2!=[]:
                result=[train1,i,train2]
                final.append(result)
    return final
#print(indirect_search(13,3,cur))
def train_lister(s):
    x=[]
    for k in s:
        for i in k[0]:
            for j in k[2]:
                x.append([i,k[1],j])
    return x
#print(train_lister([[1,2],3,[5,6]]))

def price(train_id,s1,s2,cur):
    sql='Select x,y from stations where station_id={};'.format(s1)
    cur.execute(sql);res=cur.fetchall()
    x1,y1=res[0]
    sql='Select x,y from stations where station_id={};'.format(s2)
    cur.execute(sql);res=cur.fetchall()
    x2,y2=res[0]
    distance=((x2-x1)**2 + (y2-y1)**2)**0.5
    cur.execute('select cf from trains where train_id={};'.format(train_id))
    cf=cur.fetchall()[0][0]
    cost=distance * cf
    return cost
#print(price(7,13,19,cur))
def create_identifier():
    import random
    letters='abcdefghijklmnopqrstuvwxyz'
    x=''
    for i in range(15):
        x = x + letters[random.randint(0,i)] + str(random.randint(i,30))
    return x

def stationfinder(station_id,cur):
    sql='select station_name from stations where station_id={};'.format(station_id)
    cur.execute(sql)
    res=cur.fetchall()
    return res[0][0]

def pid(name,cur):
    sql='select passenger_id from passengers where passenger_name="{}";'.format(name)
    cur.execute(sql)
    res=cur.fetchall()
    return res[0][0]


def pnrgenerator(cur):
    sql = 'select pnr_number from pnr ORDER BY booking_number DESC LIMIT 1;'
    cur.execute(sql);res=cur.fetchall()
    lastpnr =  res[0][0]
    number = int(lastpnr[1:])
    number+=1
    newpnr = lastpnr[0]+'0000'+str(number)
    return newpnr
def pidgenerator(cur):
    sql = 'select passenger_id from passengers ORDER BY passenger_id DESC LIMIT 1;'
    cur.execute(sql);res=cur.fetchall()
    number = res[0][0]
    number+=1
    return number

def bookingno(cur):
    sql = 'select booking_number from pnr ORDER BY booking_number DESC LIMIT 1;'
    cur.execute(sql);res=cur.fetchall()
    lastpnr =  res[0][0]
    newbkno = lastpnr+1
    return newbkno

def seatnumber(n):
    import random
    number = random.randint(11,120)
    nos=[]
    for i in range(n):
        nos.append(number+i)
    
    l,s = ['L','U'],['A','B']
    ln = l[random.randint(0,1)]
    sn = s[random.randint(0,1)]
    seatnumbers = []
    for i in nos:
        seatnumbers.append(sn+ln+str(i))
    return seatnumbers

