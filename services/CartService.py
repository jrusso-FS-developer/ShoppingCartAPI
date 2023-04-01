from pymongo import MongoClient
from bson.objectid import ObjectId
import json

client = MongoClient('127.0.0.1', 27017)
mongoDb = client['DevTutorialsWork'] 

class CartService:      
    def __init__(self):
        pass
    
    def get_inventory_item(self, item):  
        i_item = mongoDb.Inventory.find_one({ '_id': item }) 
        i_item = self.marshal_id(i_item)
        
        return i_item
    
    def marshal_id (self, item):
        item['_id'] = str(item['_id'])        
        return item
        
    
    def marshal_data(self, cart):
        cart = self.marshal_id(cart)
        itemsArray = []
        
        for item in cart['itemsArray']:
            itemsArray.append(self.get_inventory_item(item))
            
        cart['itemsArray'] = itemsArray
            
        return cart 
    
    def get(self, email: str):
        cart = mongoDb.Cart
        data = [self.marshal_data(cart) for cart in cart.find({ "email": email })]
        return data
    
    def delete(self, email: str, inventory_id: str):
        cart = mongoDb.Cart
        
        cart.update_one({ 'email': email }, { "$pull": { 'itemsArray': ObjectId(inventory_id) }})
        
        return self.get(email)
    
    def add(self, email: str, inventory_id: str):
        dbCart = mongoDb.Cart
        cart = self.get(email)
        
        if len(cart) == 0:
            dbCart.insert_one({ 'email': email, 'itemsArray': [ ObjectId(inventory_id) ] })            
        
        if len(cart) > 0:
            dbCart.update_one({ 'email': email }, { "$push": { 'itemsArray': ObjectId(inventory_id) }})        
        
        return self.get(email)