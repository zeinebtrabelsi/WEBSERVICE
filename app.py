from flask import Flask, jsonify 
from flask_smorest import Api
from ressources.vaccines import blp as VaccineBlueprint
from ressources.patients import blp as PatientBlueprint
from ressources.inventory import blp as InventoryBlueprint
from ressources.appointments import blp as AppointmentBlueprint
from ressources.user import blp as UserBlueprint
from db import db
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST


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
app.config["JWT_SECRET_KEY"] = "0107"
jwt = JWTManager(app)
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}
 
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )



api.register_blueprint(VaccineBlueprint)
api.register_blueprint(AppointmentBlueprint)
api.register_blueprint(InventoryBlueprint)
api.register_blueprint(PatientBlueprint)
api.register_blueprint(UserBlueprint)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
