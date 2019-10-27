# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Passengers(models.Model):
    passenger_id = models.AutoField(db_column='PASSENGER_ID', primary_key=True, blank=True)  # Field name made lowercase.
    passenger_name = models.CharField(db_column='PASSENGER_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(db_column='AGE', blank=True, null=True)  # Field name made lowercase.
    phone_number = models.BigIntegerField(db_column='PHONE_NUMBER', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'PASSENGERS'


class Pnr(models.Model):
    pnr_number = models.AutoField(db_column='PNR_NUMBER', primary_key=True, blank=True)  # Field name made lowercase.
    train_id = models.IntegerField(db_column='TRAIN_ID', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', blank=True, null=True, max_length=200)  # Field name made lowercase.
    seat_number = models.CharField(db_column='SEAT_NUMBER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='USER_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.
    passenger_id = models.IntegerField(db_column='PASSENGER_ID', blank=True, null=True)  # Field name made lowercase.
    boarding_point = models.IntegerField(db_column='BOARDING_POINT', blank=True, null=True)  # Field name made lowercase.
    boarding_time = models.TimeField(db_column='BOARDING_TIME', blank=True, null=True)  # Field name made lowercase.
    destination = models.IntegerField(db_column='DESTINATION', blank=True, null=True)  # Field name made lowercase.
    date_of_journey = models.DateField(db_column='DATE_OF_JOURNEY', blank=True, null=True)  # Field name made lowercase.
    ticket = models.FileField(db_column='TICKET', upload_to='tickets/')
    class Meta:
        managed = True
        db_table = 'PNR'


class Routes(models.Model):
    route_id = models.AutoField(db_column='ROUTE_ID', primary_key=True, blank=True)  # Field name made lowercase.
    train_id = models.IntegerField(db_column='TRAIN_ID', blank=True, null=True)  # Field name made lowercase.
    station_id = models.IntegerField(db_column='STATION_ID', blank=True, null=True)  # Field name made lowercase.
    arrival_time = models.TimeField(db_column='ARRIVAL_TIME', blank=True, null=True)  # Field name made lowercase.
    departure_time = models.TimeField(db_column='DEPARTURE_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'ROUTES'


class Stations(models.Model):
    station_id = models.AutoField(db_column='STATION_ID', primary_key=True, blank=True)  # Field name made lowercase.
    station_name = models.CharField(db_column='STATION_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    x = models.IntegerField(db_column='X', blank=True, null=True)
    y = models.IntegerField(db_column='Y', blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'STATIONS'


class Trains(models.Model):
    train_id = models.AutoField(db_column='TRAIN_ID', primary_key=True, blank=True)  # Field name made lowercase.
    train_name = models.CharField(db_column='TRAIN_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    origin = models.CharField(db_column='ORIGIN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    end_point = models.CharField(db_column='END_POINT', max_length=100, blank=True, null=True)  # Field name made lowercase.
    departure_time = models.TimeField(db_column='DEPARTURE_TIME', blank=True, null=True)  # Field name made lowercase.
    max_capacity = models.IntegerField(db_column='MAX_CAPACITY', blank=True, null=True)
    railway_classes = models.CharField(db_column='RAILWAY_CLASSES', blank=True, null=True, max_length=200)
    cf = models.IntegerField( db_column = 'CF', null = True)
    class Meta:
        managed = True
        db_table = 'TRAINS'

class metadata(models.Model):
    identifier = models.CharField(db_column = 'identifier', max_length = 100, null = True)
    pnr = models.IntegerField(db_column = 'pnr', blank = True, null = True)
    passengername = models.IntegerField(db_column = 'passengername', blank = True, null = True)
    email = models.CharField(max_length = 150, db_column = 'email', blank = True, null = True)
    traveldate = models.DateField(db_column = 'traveldate', blank = True, null = True)
    train1 = models.IntegerField(db_column = 'train1', blank = True, null = True)
    train2 = models.IntegerField(db_column = 'train2', blank = True, null = True)
    rclass = models.CharField(max_length = 150, db_column = 'rclass', blank = True, null = True)
    j = models.IntegerField(db_column = 'j', blank = True, null = True)
    seatno = models.IntegerField(db_column = 'seatno', blank = True, null = True)
    platformno = models.IntegerField(db_column = 'platformno', blank = True, null = True)
    fromid = models.IntegerField(db_column = 'fromid', blank = True, null = True)
    toid = models.IntegerField(db_column = 'toid', blank = True, null = True)
    arrival = models.DateField(db_column = 'arrival', blank = True, null = 'True')
    departure = models.DateField(db_column = 'departure', blank = True, null = 'True')
    
    class Meta:
        managed = True
        db_table = 'mdata' 



class Users(models.Model):
    user_id = models.CharField(db_column='USER_ID', primary_key=True, max_length=20, blank=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='USER_NAME', max_length=100)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'USERS'