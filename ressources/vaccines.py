import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import VaccineModel
from schemas import VaccineSchema

from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("vaccines", __name__, description="Operations on vaccines")

@blp.route("/vaccine")
class VaccineList(MethodView):
    # GET method to retrieve all vaccines
    @blp.response(200, VaccineSchema(many=True))  
    def get(self):
        return VaccineModel.query.all()

    # POST method to create a new vaccine
    @blp.arguments(VaccineSchema)  
    @blp.response(201, VaccineSchema) 
    def post(self, vaccine_data):
        
        existing_vaccine = VaccineModel.query.filter_by(vaccine_name=vaccine_data["vaccine_name"]).first()
        if existing_vaccine:
            abort(400, message="Vaccine already exists.")

        
        vaccine = VaccineModel(**vaccine_data)
        try:
            db.session.add(vaccine)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message="An error occurred while adding the vaccine.")
        return vaccine

@blp.route("/vaccine/<string:vaccine_id>")
class Vaccine(MethodView):
    # GET method to retrieve a specific vaccine by ID
    @blp.response(200, VaccineSchema)  
    def get(self, vaccine_id):
        vaccine = VaccineModel.query.get(vaccine_id)
        if not vaccine:
            abort(404, message="Vaccine not found.")
        return vaccine
    
    # DELETE method to delete a specific vaccine by ID
    def delete(self, vaccine_id):
        vaccine = VaccineModel.query.get(vaccine_id)
        if not vaccine:
            abort(404, message="Vaccine not found.")

        db.session.delete(vaccine)
        db.session.commit()
        return {"message": "Vaccine deleted."}
