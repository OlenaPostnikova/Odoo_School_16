from odoo import models, fields


class HrHospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Hospital patient'

    name = fields.Char(required=True)
    active = fields.Boolean(
        default=True, )
