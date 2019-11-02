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


def dateify(date_str):
    import datetime
    d=date_convert(date_str);d=str(d)
    date=datetime.date(int(d[:4]),int(d[4:6]),int(d[6:]))
    return date
