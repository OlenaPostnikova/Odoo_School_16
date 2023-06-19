from odoo import models, fields


class HrHospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Hospital doctor'

    name = fields.Char(required=True)
    active = fields.Boolean(
        default=True, )
    specialization = fields.Char(required=True)
