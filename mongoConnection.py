import pymongo


def connectToMongo(host="localhost", port=27017, ignore_unicode_error=False):
    if ignore_unicode_error:
        mongoConnection = pymongo.MongoClient(host, port, unicode_decode_error_handler='ignore')
    else:
        mongoConnection = pymongo.MongoClient(host, port)
    return mongoConnection

def closeMongo(connection):
    connection.close()
