from mongorm import Document
from player_pb2 import Player as _pb


class Player(Document):
    _message = _pb
    _database = 'test1'
    _collection = 'player'


if __name__ == '__main__':
    player = Player()
    player.insert_one({'name': 'jack', 'age': 10})
    # mgo = pymongo.MongoClient()
    # db = mgo.get_database('test')
    # db.authenticate('zh', '123321')
    # col = db.get_collection('test')
    # col.insert_one({'name': 'jack', 'age': 10})
