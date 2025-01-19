import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import AppointmentModel, VaccineModel, PatientModel
from schemas import AppointmentSchema, AppointmentUpdateSchema
from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("appointments", __name__, description="Operations on appointments")

# Class-based view to handle all appointments
@blp.route("/appointments")
class AppointmentList(MethodView):
    # GET method to retrieve all appointments
    @jwt_required()
    @blp.response(200, AppointmentSchema(many=True))
    def get(self):
        return AppointmentModel.query.all()

    # POST method to create a new appointment
    @blp.arguments(AppointmentSchema)
    @blp.response(201, AppointmentSchema)
    def post(self, appointment_data):
        # check if the vaccine exists
        vaccine = VaccineModel.query.get(appointment_data["vaccine_id"])
        if not vaccine:
            abort(404, message="Vaccine not found.")
        # check if the patient already exists
        patient = PatientModel.query.filter_by(contact_info=appointment_data["contact_info"]).first()
        if not patient:
            patient_data = {
                "patient_name": appointment_data["patient_name"],
                "contact_info": appointment_data["contact_info"],
            }
            patient = PatientModel(**patient_data)
            try:
                db.session.add(patient)
                db.session.commit()
            except SQLAlchemyError as e:
                abort(400, message="An error occurred while adding the patient.")
        existing_appointment = AppointmentModel.query.filter_by(contact_info=appointment_data["contact_info"]).first()
        if existing_appointment:
           abort(400, message="Appointment already exists for this contact.")
        appointment_date = appointment_data.get("date")
        if not appointment_date:
           from datetime import date
           appointment_date = date.today()
        appointment_data["patient_id"] = patient.id
        appointment = AppointmentModel(
            patient_name=appointment_data["patient_name"],
            vaccine_id=appointment_data["vaccine_id"],
            contact_info=appointment_data["contact_info"],
            patient_id=patient.id,
            date=appointment_date,
        )
        

        try:
            db.session.add(appointment)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e))
            abort(400, message="An error occurred while adding the appointment.")
        return appointment, 201
    

@blp.route("/appointments/<string:appointment_id>")
class Appointment(MethodView):
    # GET method to retrieve an appointment by appointment ID
    @jwt_required()
    @blp.response(200, AppointmentSchema)
    def get(self, appointment_id):
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            abort(404, message="Appointment not found.")

        return appointment

    # PUT method to update appointment status by appointment ID
    @blp.arguments(AppointmentUpdateSchema)
    @blp.response(200, AppointmentSchema)
    def put(self, appointment_data, appointment_id):
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            abort(404, message="Appointment not found.")
        for key, value in appointment_data.items():
            setattr(appointment, key, value)
        db.session.commit()
        return appointment

    # DELETE method to delete an appointment by appointment ID
    def delete(self, appointment_id):
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            abort(404, message="Appointment not found.")
        db.session.delete(appointment)
        db.session.commit()
        return {"message": "Appointment deleted successfully"}