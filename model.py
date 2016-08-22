from enum import Enum
from datetime import datetime, timedelta
from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, DateTimeField, Field

db = SqliteDatabase('pysn.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    sso = CharField(unique=True)

class APIToken(BaseModel):
    value = CharField(unique=True)
    expiry_date = DateTimeField()

    @property
    def expired():
        return expiry_date > datetime.now()

class AccessToken(APIToken):
    user = ForeignKeyField(User, related_name='access_token')

class RefreshToken(APIToken):
    access_token = ForeignKeyField(AccessToken, related_name='refresh_token')

class Device(BaseModel):
    # apple push notification system device token
    apns_token = CharField(unique=True)
    # one-to-many relationship between a user and his/her devices
    user = ForeignKeyField(User, related_name='devices')

def create_tables():
    db.connect()
    db.create_tables([User, AccessToken, RefreshToken, Device], safe=True)
