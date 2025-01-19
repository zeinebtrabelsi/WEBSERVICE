import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import PatientModel
from schemas import PatientSchema
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required


blp = Blueprint("patients", __name__, description="Operations on patients")


@blp.route("/patient")
class PatientList(MethodView):
    @jwt_required()
    @blp.response(200, PatientSchema(many=True))  
    def get(self):
        return PatientModel.query.all()

    # POST method to create a new patient
    @blp.arguments(PatientSchema) 
    @blp.response(201, PatientSchema) 
    def post(self, patient_data):
        
        existing_patient = PatientModel.query.filter_by(contact_info=patient_data["contact_info"]).first()
        if existing_patient:
            abort(400, message="Patient already exists.")

        
        patient = PatientModel(**patient_data)
        try:
            db.session.add(patient)
            db.session.commit()
        except SQLAlchemyError :
            abort(400, message="An error occurred while adding the patient.")

        return patient


@blp.route("/patient/<string:patient_id>")
class Patient(MethodView):
    @jwt_required()
    @blp.response(200, PatientSchema) 
    def get(self, patient_id):
        patient = PatientModel.query.get(patient_id)
        if not patient:
            abort(404, message="Patient not found.")
        return patient

    # DELETE method to delete a specific patient by ID
    def delete(self, patient_id):
        patient = PatientModel.query.get(patient_id)
        if not patient:
            abort(404, message="Patient not found.")
        
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted."}

    # PUT method to update a specific patient's information
    @blp.arguments(PatientSchema)  
    @blp.response(201, PatientSchema)  
    def put(self, patient_data, patient_id):
        patient = PatientModel.query.get(patient_id)
        if not patient:
            abort(404, message="Patient not found.")

        
        patient.patient_name = patient_data.get("patient_name", patient.patient_name)
        patient.contact_info = patient_data.get("contact_info", patient.contact_info)
        db.session.commit()

        return patient
