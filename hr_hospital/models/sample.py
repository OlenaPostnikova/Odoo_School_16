from odoo import models, fields


class HrHospitalSample(models.Model):
    _name = 'hr_hospital.sample'
    _description = 'Sample'

    name = fields.Char()
    active = fields.Boolean(
        default=True, )
    sample_type_id = fields.Many2one('hr_hospital.sample.type')