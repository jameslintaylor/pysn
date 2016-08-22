from enum import Enum
from datetime import datetime, timedelta
from peewee import SqliteDatabase, Model, CharField, ForeignKeyField, DateTimeField, Field

from psn import PSNToken

db = SqliteDatabase('pysn.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    sso = CharField(unique=True)
    access_token = CharField(unique=True)
    access_token_expiry = DateTimeField()
    refresh_token = CharField(unique=True)
    refresh_token_expiry = DateTimeField()

    @property
    def access_token(self):
        if access_token and access_token_expiry:
            return PSNToken(access_token, access_token_expiry)
        else:
            return None

    @property
    def refresh_token(self):
        if refresh_token and refresh_token_expiry:
            return PSNToken(refresh_token, refresh_token_expiry)
        else:
            return None

class Device(BaseModel):
    # apple push notification system device token
    apns_token = CharField(unique=True)
    # one-to-many relationship between a user and his/her devices
    user = ForeignKeyField(User, related_name='devices')

def create_tables():
    db.connect()
    db.create_tables([User, Device], safe=True)
