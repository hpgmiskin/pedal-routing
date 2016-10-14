import mongoengine

from .accident import Accident

class Database:

    def __init__(self):
        self.Accident = Accident

    def connect(self,host = 'mongodb://localhost:27017/pedal-together'):
        mongoengine.connect('tx', host = host)


if (__name__ == '__main__'):
    database = Database()
    database.connect()