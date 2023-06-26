from odoo import models, fields


class HrHospitalContactPerson(models.AbstractModel):
    _name = 'hr_hospital.contact_person'
    _description = 'Hospital contact_person'

    name = fields.Char()
    telephone_number = fields.Char()
    email = fields.Char()
    photo = fields.Image(max_width=256, max_height=256)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ],  default='female')