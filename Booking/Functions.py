#import mysql.connector
#con=mysql.connector.connect(host='localhost',user='root',passwd='root',database='travelx')
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

def namefinder(train_id,cur):
    '''Takes int(train id) and returns the train name as str'''
    sql='select train_name from trains where train_id={};'.format(train_id)
    cur.execute(sql)
    res=cur.fetchall()
    train_name=res[0][0]
    return train_name

def timings(train_id,f,t,cur):
    '''Returns tuple of strings as (arrival,departure)'''
    sql1='select departure_time from routes where train_id={} and station_id={};'
    cur.execute(sql1.format(train_id,f))
    res=cur.fetchall()
    depart=str(res[0][0])
    sql2='select arrival_time from routes where train_id={} and station_id={};'
    cur.execute(sql2.format(train_id,t))
    res=cur.fetchall()
    arrive=str(res[0][0])
    return arrive,depart
#print(timings(7,3,5,cur))

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
    junctions=[1,6,7,5,13]
    for i in junctions:
        train1=direct_search(f,i,cur)
        if train1!=[]:
            train2=direct_search(i,t,cur)
            if train2!=[]:
                result=[train1,i,train2]
                return result
    return []
