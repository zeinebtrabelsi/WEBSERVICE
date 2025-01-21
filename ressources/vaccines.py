import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import VaccineModel
from schemas import VaccineSchema
from datetime import date
from flask_mail import Mail, Message
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint("vaccines", __name__, description="Operations on vaccines")

@blp.route("/vaccine")
class VaccineList(MethodView):
    # GET method to retrieve all vaccines
    @blp.response(200, VaccineSchema(many=True))  
    def get(self):
        vaccines = VaccineModel.query.all()
        today = date.today()
        in_demand_vaccines = [
            vaccine for vaccine in vaccines
            if vaccine.demand_start_date and vaccine.demand_end_date
            and vaccine.demand_start_date <= today <= vaccine.demand_end_date
        ]

        
        if in_demand_vaccines:
            email_body = """
            <html>
                <body>
                    <p>The following vaccines are in high demand during this period:</p>
                    <table border="1" cellpadding="5" cellspacing="0">
                        <tr>
                            <th>Vaccine Name</th>
                            <th>Recommended Age Group</th>
                            <th>Demand Start Date</th>
                            <th>Demand End Date</th>
                        </tr>
            """
            for vaccine in in_demand_vaccines:
                email_body += f"""
                    <tr>
                        <td>{vaccine.vaccine_name}</td>
                        <td>{vaccine.recommended_age_group}</td>
                        <td>{vaccine.demand_start_date}</td>
                        <td>{vaccine.demand_end_date}</td>
                    </tr>
                """
            email_body += """
                    </table>
                    <p>Keep your inventory steady and stay informed!</p>
                </body>
            </html>
            """
        else:
            email_body = """
            <html>
                <body>
                    <p>No vaccines are in high demand during this period. Keep your inventory steady.</p>
                </body>
            </html>
            """

        
        mail = Mail()
        msg = Message(
            "Vaccine Demand Notification",
            sender="trabelsizeineb@tbs.u-tunis.tn",
            recipients=["zeineb.trabelsi2609@gmail.com"],
            html=email_body,  
        )
        mail.send(msg)

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
