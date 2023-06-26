from odoo import models, fields

class HrHospitalDiseaseGroup(models.Model):
    _name = 'hr_hospital.disease_group'
    _description = 'Hospital disease groups'

    name = fields.Char(required=True)
    active = fields.Boolean(
        default=True, )
