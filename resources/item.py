import sqlite3
from flask import Flask,jsonify,request
from flask_restful import Resource, Api,reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate,identity
#from user import UserRegister
from models.item import ItemModel



class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannoy be left blank")
    parser.add_argument('store_id',type=int,required=True,help="Every item needs a store a id")

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'},404
        
        #item = next(filter(lambda item:item['name']==name,items),None)
        #return {'item': item}, 200 if item else 404  # not found




    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)},400
        data= Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message":"An error occured inserting the item."},500
        return item.json(), 201 # quando crear algum item

   
    @jwt_required()
    def delete(self,name):
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()
#
        #query = "DELETE FROM items WHERE name=?"
        #cursor.execute(query,(name,))
        #connection.commit()
    #
        #connection.close()
#
        #return {'message':'Item deleted'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'}



    def put(self,name):
        data= Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        #if item is None:
        #    try:
        #        update_item.insert()
        #    except:
        #        return {"message":"An error occured inserting the item."},500
        #else:
        #    try:
        #        update_item.update()
        #    except:
        #             return {"message":"An error occured inserting the item."},500
        #return update_item.json()
        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']
        item.save_to_db()
                     
        return item.json()





class ItemList(Resource):
    def get(self):
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()
#
        #query = "SELECT * FROM items"
        #results = cursor.execute(query)
        #items=[]
        #for row in results:
        #    items.append({"name":row[0],'price':row[1]})
        #
    #
        #connection.close()
        #return {'items':items}
        return {'items':[x.json() for x in ItemModel.query.all()]}
        