from datetime import datetime, timedelta

from peewee import BooleanField, CharField, DateTimeField, ForeignKeyField, Model, TextField
from playhouse.postgres_ext import ArrayField

from src import app


class BaseModel(Model):
    class Meta:
        database = app.database


class UserTb(BaseModel):
    name = CharField(unique=True)
    password = CharField()
    ip = ArrayField(CharField, null=True)


class ApiKey(BaseModel):
    public_key = TextField(unique=True)
    private_key = TextField(unique=True)
    is_active = BooleanField(default=True)
    activation_time = DateTimeField(default=datetime.now())
    deactivation_time = DateTimeField(default=datetime.now() + timedelta(days=30))
    fk_user = ForeignKeyField(UserTb)


class OneTimePass(BaseModel):
    creation_time = DateTimeField(default=datetime.now())
    is_activated = BooleanField(default=False)
    password = CharField(unique=True)
    activation_time = DateTimeField(null=True)
    activation_ip = CharField(max_length=16, null=True)
    generated_user = ForeignKeyField(UserTb, null=True)
    generated_key = ForeignKeyField(ApiKey, null=True)
    expiration_time = DateTimeField(default=datetime.now() + timedelta(hours=12))


all_models = [UserTb, ApiKey, OneTimePass]
