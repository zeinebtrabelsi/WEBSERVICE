import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import InventoryModel, VaccineModel
from schemas import InventorySchema, InventoryUpdateSchema

blp = Blueprint("inventory", __name__, description="Operations on vaccine inventory")

@blp.route("/inventory")
class InventoryList(MethodView):
    # GET method to retrieve all inventory items
    @blp.response(200, InventorySchema(many=True))  
    def get(self):
        return InventoryModel.query.all()

    # POST method to create a new inventory item
    @blp.arguments(InventorySchema)  
    @blp.response(201, InventorySchema)  
    def post(self, inventory_data):
        vaccine = VaccineModel.query.get(inventory_data["vaccine_id"])
        if not vaccine:
            abort(404, message="Vaccine not found.")
        inventory_item = InventoryModel(
            vaccine_id=inventory_data["vaccine_id"],
            stock_level=inventory_data["stock_level"]
        )
        db.session.add(inventory_item)
        db.session.commit()

        return inventory_item, 201
@blp.route("/inventory/<int:inventory_id>")
class InventoryItem(MethodView):
    # DELETE method to delete an inventory item by ID
    def delete(self, inventory_id):
        inventory_item = InventoryModel.query.get(inventory_id)
        if not inventory_item:
            abort(404, message="Inventory item not found.")

        db.session.delete(inventory_item)
        db.session.commit()
        return {"message": "Inventory item deleted."}

    # PUT method to update an inventory item by ID
    @blp.arguments(InventoryUpdateSchema) 
    @blp.response(200, InventorySchema)  
    def put(self, inventory_data, inventory_id):
        inventory_item = InventoryModel.query.get(inventory_id)
        if not inventory_item:
            abort(404, message="Inventory item not found.")

        
        inventory_item.stock_level = inventory_data["stock_level"]
        db.session.commit()

        return inventory_item