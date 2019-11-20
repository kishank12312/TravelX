from django import template
from Booking import Functions

register = template.Library()

@register.filter
def index(value,i):
    index=int(i)
    return value[index]


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