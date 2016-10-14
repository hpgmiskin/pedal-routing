import datetime
from mongoengine import *
    
class Accident(Document):

    accid = IntField(unique=True)

    age = IntField()
    severity = StringField()
    location = PointField()
    date = DateTimeField()

    roadtype = StringField()
    junctionDetail = StringField()
    lightConditions = StringField()
    weatherConditions = StringField()
    roadSurfaceConditions = StringField()
    roadUser = StringField()


    meta = dict(
        collection = 'accidents'
    )

    