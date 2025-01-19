from marshmallow import Schema, fields

class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_name = fields.Str(required=True)
    contact_info = fields.Str(required=True)
    vaccine_id = fields.Int(required=True)
    status = fields.String(default="Scheduled")
    date = fields.Date(required=True) 
    vaccine_name=fields.String(attribute='vaccine.vaccine_name',dump_only=True)

class AppointmentUpdateSchema(Schema):
    status=fields.Str(required=True)

class InventorySchema(Schema):
    id = fields.Int(dump_only=True)
    vaccine_id = fields.Int(required=True)
    stock_level = fields.Int(required=True)
    vaccine_name = fields.String(attribute='vaccine.vaccine_name',dump_only=True)

class InventoryUpdateSchema(Schema):
    stock_level= fields.Int(required=True)
    

class PatientSchema(Schema):
    id = fields.Int(dump_only=True)
    patient_name = fields.Str(required=True)
    contact_info = fields.Str(required=True)


class VaccineSchema(Schema):
    id = fields.Int(dump_only=True)  # Field for the vaccine's unique ID
    vaccine_name = fields.Str(required=True)  # Field for the vaccine name
    manufacturer = fields.Str()  # Field for manufacturer
    side_effects = fields.Str()  # Field for side effects
    recommended_age_group = fields.Str()  # Field for age group
    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)