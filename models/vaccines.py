from db import db
import datetime

class VaccineModel(db.Model):
    __tablename__ = "vaccines"

    id = db.Column(db.Integer, primary_key=True)
    vaccine_name = db.Column(db.String(80), unique=True, nullable=False)
    manufacturer = db.Column(db.String(80), nullable=False)
    recommended_age_group = db.Column(db.String(80), nullable=False)
    side_effects = db.Column(db.String(255), nullable=False)
    demand_start_date = db.Column(db.Date, nullable=False)  
    demand_end_date = db.Column(db.Date, nullable=False)
    appointments = db.relationship("AppointmentModel", back_populates="vaccine", lazy="dynamic")

   
    inventory = db.relationship("InventoryModel", back_populates="vaccine", lazy="dynamic")
