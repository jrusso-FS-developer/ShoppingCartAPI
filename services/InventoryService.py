from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
mongoDb = client['DevTutorialsWork'] 

class InventoryService:      
    def __init__(self):
        pass
    
    def marshal_data(self, item):
        item['_id'] = str(item['_id'])
        return item 
    
    def get(self):
        items = mongoDb.Inventory
        data = [self.marshal_data(item) for item in items.find()]
        return data