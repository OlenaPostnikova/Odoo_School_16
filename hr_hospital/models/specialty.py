from odoo import models, fields


class HrHospitalSpecialty(models.Model):
    _name = 'hr_hospital.specialty'
    _description = 'Medical specialty'

    name = fields.Char(required=True)
    active = fields.Boolean(
        default=True, )
