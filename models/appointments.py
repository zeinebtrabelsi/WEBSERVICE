from db import db
from datetime import date 
class AppointmentModel(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    vaccine_id = db.Column(db.Integer, db.ForeignKey("vaccines.id"))
    patient_name = db.Column(db.String(80), nullable=False)
    contact_info = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), default="scheduled")
    date = db.Column(db.Date, nullable=False)

    # Relationships
    patient = db.relationship("PatientModel", back_populates="appointments")
    vaccine = db.relationship("VaccineModel", back_populates="appointments")

   