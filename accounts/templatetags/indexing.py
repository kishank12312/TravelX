from django import template
from Booking import Functions
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
def index(value,i):
    index=int(i)
    return value[index]

@register.filter
def idfinder(value):
    import mysql.connector
    con=mysql.connector.connect(host='localhost',user='root',passwd='root',database='travelxdb')
    cur=con.cursor()
    '''Takes int(train id) and returns the train name as str'''
    sql='select train_name from trains where train_id={};'.format(int(value))
    cur.execute(sql)
    res=cur.fetchall()
    train_name=res[0][0]
    return train_name


@register.filter
def stationname(value): 
    import mysql.connector
    con=mysql.connector.connect(host='localhost',user='root',passwd='root',database='travelxdb')
    cur=con.cursor()
    sql='select station_name from stations where station_id={};'.format(value)
    cur.execute(sql)
    res=cur.fetchall()
    return res[0][0]
    

@register.filter
def dictindex(value,i): 
    return value.get(i)


@register.filter
def station_name(value):
    import mysql.connector
    con=mysql.connector.connect(host='localhost',user='root',passwd='root',database='travelxdb')
    cur=con.cursor()
    name = Functions.stationfinder(value,cur)
    return name


@register.filter
def direct_check(value):
    if value == [[], [], [], [], [], [], []]:
        return False
    else:
        return True


@register.filter
def trange(value):
    value=int(value)
    l=[]
    for i in range(value):
        l.append(i)
    return l