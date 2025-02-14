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
    id = fields.Int(dump_only=True)  
    vaccine_name = fields.Str(required=True)  
    manufacturer = fields.Str()  
    side_effects = fields.Str()  
    recommended_age_group = fields.Str() 
    demand_start_date = fields.Date(required=True) 
    demand_end_date = fields.Date(required=True) 
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)