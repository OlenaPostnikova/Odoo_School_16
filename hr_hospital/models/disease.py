from odoo import models, fields

class HrHospitalDisease(models.Model):
    _name = 'hr_hospital.disease'
    _description = 'Hospital disease'

    name = fields.Char(required=True)
    active = fields.Boolean(
        default=True, )
# parent
    disease_group_id = fields.Many2one('hr_hospital.disease_group')