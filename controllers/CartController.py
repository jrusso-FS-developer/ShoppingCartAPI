from flask import Flask, request
from flask_restx import Resource, Api
from decorators.AuthDecorator import requires_auth
from services.CartService import CartService 
from bson import json_util

app = Flask(__name__)
api = Api(app)

@api.route("/cart")
class CartController(Resource):   
    
    def marshal_data(self, item):
        item['_id'] = str(item['_id'])
        return item  
 
    @requires_auth
    def get(self):  
        cartService = CartService()
        email = request.args.get("email")  
        data: list = None
          
        if email is not None:
            data = cartService.get(email)
        
        if len(data) == 0:
            return "Record not found", 404
        else:
            return data
 
    @requires_auth
    def delete(self):  
        cartService = CartService()
        email = request.args.get("email")  
        inventory_id = request.args.get("inventory_id")  
        data: list = None
          
        if email is not None and inventory_id is not None:
            data = cartService.delete(email, inventory_id)
        
        return data
        
    @requires_auth
    def post(self):
        cartService = CartService()
        email = request.args.get("email")  
        inventory_id = request.args.get("inventory_id")  
        data: list = None
          
        if email is not None and inventory_id is not None:
            data = cartService.add(email, inventory_id)
        
        return data