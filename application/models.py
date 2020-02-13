import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone

# Current time in UTC
now_utc = datetime.now(timezone('US/Eastern'))
now_local = now_utc.astimezone(get_localzone())


class Fullfilment_center(db.Document):
    fc_id = db.IntField( unique=True )
    fc_name = db.StringField( max_lenght=50 )
    fc_address = db.StringField( max_length=75 )
    fc_city = db.StringField( max_length=25 )
    fc_zip = db.StringField( max_length=5 )

class Company(db.Document):
    company_id = db.IntField( unique=True )
    fc_id = db.IntField()
    company_name = db.StringField( max_lenght=50 )
    email = db.EmailField( max_lenght=30, unique=True )
    password = db.StringField()
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def get_password(self, password):
        return check_password_hash(self.password, password)        
    
class Van(db.Document):
    van_id = db.IntField( unique=True )
    company_name = db.StringField()
    vin = db.StringField( unique=True )
    
class Schedule_wave(db.Document):
    wave_id = db.IntField( unique=True )
    company_id = db.IntField()
    start_time = db.DateTimeField( default=now_local )
    end_time = db.DateTimeField( default=now_local )
    status = db.BooleanField( default=True )
    
class Activity(db.Document):
    act_id = db.IntField( unique=True )
    vin = db.StringField()
    scan_time = db.DateTimeField( default=now_local )
