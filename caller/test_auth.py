from pymongo import MongoClient

username = 'zh'
password = '123321'
mgo = MongoClient('mongodb://127.0.0.1')

db = mgo['test']
db.authenticate(username, password)
col = db['test']
players = col.find({})
for p in players:
    print(p)
