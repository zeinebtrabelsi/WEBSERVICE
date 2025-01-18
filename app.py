from flask import Flask
from flask_smorest import Api
from ressources.vaccines import blp as VaccineBlueprint
from ressources.patients import blp as PatientBlueprint
from ressources.inventory import blp as InventoryBlueprint
from ressources.appointments import blp as AppointmentBlueprint
from db import db



app = Flask(__name__)


app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Vaccination management system for INSTITUT PASTEUR"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vaccinedata.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
api = Api(app)
 
api.register_blueprint(VaccineBlueprint)
api.register_blueprint(AppointmentBlueprint)
api.register_blueprint(InventoryBlueprint)
api.register_blueprint(PatientBlueprint)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
