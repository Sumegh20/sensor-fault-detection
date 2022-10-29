import pymongo
from sensor.constant.database import DATABASE_NAME
import certifi
ca = certifi.where()

def getMongoDBURL():
    path_to_file = '/home/cloudcraftz/test/iNeuron/mongodbURL.txt'
    with open(path_to_file) as f:
        url = f.readline()

    return url.replace('\n','')

class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url  =  getMongoDBURL()
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e