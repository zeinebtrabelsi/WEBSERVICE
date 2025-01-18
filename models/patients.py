from db import db
import uuid

class PatientModel(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(80), nullable=False)
    contact_info = db.Column(db.String(80), nullable=False)

    # One-to-Many relationship with AppointmentModel
    appointments = db.relationship("AppointmentModel", back_populates="patient", lazy="dynamic")