from odoo import models, fields


class HrHospitalDoctor(models.Model):
    _name = 'hr_hospital.doctor'
    _description = 'Hospital doctors'
    _inherit = 'hr_hospital.personaldata'

    name = fields.Char(required=True)
    active = fields.Boolean(
        default=True, )

#   speciality
    specialty_id = fields.Many2one(comodel_name='hr_hospital.specialty', string='Specialty')
#   text comment
    specialization = fields.Char(required=False)

#intern & mentor
    is_intern = fields.Boolean('is intern')
    intern_ids = fields.One2many(comodel_name='hr_hospital.doctor',
                                 inverse_name='mentor_id',
                                 domain=[('is_intern', '=', True)])
    mentor_id = fields.Many2one(comodel_name='hr_hospital.doctor',
                                string='Mentor',
                                domain=[('is_intern', '=', False)])

    #for wizard new doctor
    patient_ids = fields.One2many(comodel_name='hr_hospital.patient',
                              inverse_name='doctor_id')