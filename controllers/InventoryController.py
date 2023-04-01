from flask import Flask, request, json
from flask_restx import Resource, Api
from decorators.AuthDecorator import requires_auth
from services.CartService import CartService 
from services.InventoryService import InventoryService 

app = Flask(__name__)
api = Api(app)

@api.route("/inventory")
class InventoryController(Resource):   
    
    def marshal_data(self, item):
        item['_id'] = str(item['_id'])
        return item  
 
    def get(self):  
        inventoryService = InventoryService()
        data: list = None
          
        data = inventoryService.get()
        
        if len(data) == 0:
            return "Record not found", 404
        else:
            return data