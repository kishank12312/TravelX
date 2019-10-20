import mysql.connector

con=mysql.connector.connect(host='localhost',user='root',passwd='root',database='db2')
cur=con.cursor()
def date_convert(date):
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month_nos=['01','02','03','04','05','06','07','08','09','10','11','12']
    i=months.index(date[:3]);month=month_nos[i]
    comma=date.find(',')
    day=date[4:comma]
    year=date[len(date)-4:len(date)]
    date_formatted=int(str(year)+str(month)+str(day))
    return date_formatted

def convert_id(ft,tt):
    text='select station_id from stations where station_name="{}";'
    names,ids=[ft,tt],[]
    for i in range(2):
        x=cur.execute(text.format(names[i]))
        res=cur.fetchall()
        res=res[0][0]
        ids.append(res)
    return (ids[0],ids[1])


def direct_search(f,t):
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

def indirect_search(f,t):
    junctions=[1,6,7,5,13]
    for i in junctions:
        train1=direct_search(f,i)
        if train1!=[]:
            train2=direct_search(i,t)
            if train2!=[]:
                result=[train1,i,train2]
                return result
    return []











