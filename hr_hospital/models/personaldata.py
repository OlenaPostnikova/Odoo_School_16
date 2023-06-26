from odoo import models, fields, api

class HrHospitalPersonalData(models.AbstractModel):
    _name = 'hr_hospital.personaldata'
    _description = 'Hospital personal data'

    first_name = fields.Char()
    middle_name = fields.Char()
    family_name = fields.Char()
    name = fields.Char(compute='_compute_full_name')

    phone_number = fields.Char()
    email = fields.Char()
    photo = fields.Image(max_width=256, max_height=256)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], default='female')

    @api.depends('first_name')
    def _compute_full_name(self):
        for rec in self:
            rec.name = '%s %s %s' % \
                    (rec.family_name , rec.first_name, rec.middle_name)
