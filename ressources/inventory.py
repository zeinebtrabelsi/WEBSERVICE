import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import InventoryModel, VaccineModel
from schemas import InventorySchema, InventoryUpdateSchema
from flask_mail import Message, Mail
import matplotlib.pyplot as plt
import io
from flask import send_file
blp = Blueprint("inventory", __name__, description="Operations on vaccine inventory")

@blp.route("/inventory")
class InventoryList(MethodView):
    # GET method to retrieve all inventory items
    @blp.response(200, InventorySchema(many=True))  
    def get(self):
     # Retrieve all inventory items
        inventory_items = InventoryModel.query.all()
         # Retrieve all inventory items
        inventory_items = InventoryModel.query.all()

        # Prepare data for the chart
        vaccine_names = [item.vaccine.vaccine_name for item in inventory_items]
        stock_levels = [item.stock_level for item in inventory_items]

        # Create a bar chart with vaccine names on the X-axis and stock levels on the Y-axis
        plt.figure(figsize=(10, 6))
        plt.bar(vaccine_names, stock_levels)
        plt.xlabel('Vaccine Name')
        plt.ylabel('Stock Level')
        plt.title('Inventory Stock Levels')
        plt.xticks(rotation=45, ha="right")  # Rotate vaccine names for better readability

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
        
        # Send the chart as a response
        return send_file(img, mimetype='image/png', as_attachment=False, download_name='inventory_chart.png')

        # Filter inventory items with stock_level below 100
        low_stock_items = [
            item for item in inventory_items
            if item.stock_level < 100
        ]

        # Compose email with HTML table
        if low_stock_items:
            email_body = """
            <html>
                <body>
                    <p>These vaccines are facing shortage. Please update your stock:</p>
                    <table border="1" cellpadding="5" cellspacing="0">
                        <tr>
                            <th>Vaccine Name</th>
                            <th>Stock Level</th>
                        </tr>
            """
            for item in low_stock_items:
                vaccine_name = item.vaccine.vaccine_name  # Get the vaccine name from the related VaccineModel
                email_body += f"""
                    <tr>
                        <td>{vaccine_name}</td>
                        <td>{item.stock_level}</td>
                    </tr>
                """
            email_body += """
                    </table>
                    <p>It is important to maintain proper inventory levels to ensure continuous availability of vaccines. Please take the necessary action.</p>
                </body>
            </html>
            """
        else:
            email_body = """
            <html>
                <body>
                    <p>All inventory items have sufficient stock levels.</p>
                </body>
            </html>
            """

        # Send the email (example setup with Flask-Mail)
        mail = Mail()
        msg = Message(
            "Inventory Stock Level Alert",
            sender="trabelsizeineb@tbs.u-tunis.tn",
            recipients=["zeineb.trabelsi2609@gmail.com"],
            html=email_body,  # Send the email body as HTML
        )
        mail.send(msg)

        # Return all inventory items
        return inventory_items
   

    # POST method to create a new inventory item
    @blp.response(201, InventorySchema)  
    @blp.arguments(InventorySchema)
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

      

        return inventory_item

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