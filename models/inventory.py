from db import db
from models import VaccineModel

class InventoryModel(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    stock_level = db.Column(db.Integer, nullable=False)
    vaccine_id = db.Column(db.Integer, db.ForeignKey("vaccines.id"), nullable=False)
    # Relationship with VaccineModel
    vaccine = db.relationship("VaccineModel", back_populates="inventory")

    