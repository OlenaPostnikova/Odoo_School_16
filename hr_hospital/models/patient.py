from datetime import date
from odoo import models, fields, api


class HrHospitalPatient(models.Model):
    _name = 'hr_hospital.patient'
    _description = 'Hospital patient'
    _inherit = 'hr_hospital.personaldata'

    name = fields.Char(required=True)
    active = fields.Boolean(
        default=True, )
    birthday = fields.Date('Date of Birth')

    # error tracking - ???
    age = fields.Integer(compute='_compute_age')
    passport_id = fields.Char(string='Passport No')
    passport_date = fields.Date('Date of passport issue')
    passport_authority = fields.Char('Authority')
    # doctor, contact
    partner_id = fields.Many2one(comodel_name='res.partner', string='Emergency contact')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Current doctor')
    # history, visits (One2many)
    doctor_history_ids = fields.One2many(comodel_name='hr_hospital.doctor.history',
                                         inverse_name='patient_id')
    visit_ids = fields.One2many(comodel_name='hr_hospital.visit',
                                inverse_name='patient_id')
    disease_ids = fields.Many2many(comodel_name='hr_hospital.disease')
    #add samples ?
    grade_of_sick = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    ], tracking=True, default='1')

    @api.depends('birthday')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.birthday:
                rec.age = today.year - rec.birthday.year
            else:
                rec.age = 1

    # re-write - onchange - to function Write
    @api.onchange('doctor_id')
    def onchange_doctor_id(self):
        print('-------------------method onchange doctor_id----------------------')
        #example: add record to other table
        # for rec in self:
        #     lines = []
        #     valstruct = {
        #         'date': date.today(),
        #         'patient_id': rec.id,
        #         'doctor_id': rec.doctor_id
        #     }
        #     lines.append((0, 0, valstruct))
        #     rec.doctor_history_ids = lines

    def write(self, vals):
        if 'doctor_id' in vals:
            print('-------------------doctor_id_in_vals----------------------')
            for rec in self:
                if rec.doctor_id != vals.get('doctor_id'):
                    # if old doctor != new doctor
                    new_vals_doctor_history = {
                        'date': date.today(),
                        'patient_id': rec.id,
                        'doctor_id': vals.get('doctor_id')
                    }
                    rec.doctor_history_ids.create(new_vals_doctor_history)
        else:
            print('-------------------doctor_id_NOT_in_vals----------------------')

        #attention: as method write was redefined we need to finish writing manually (1C => return status = 0 )
        res = super(HrHospitalPatient, self).write(vals)

    #find visit with diagnosis of this disease
    def get_diagnosis_date(self, disease_id):
        self.ensure_one()
        for rec_visit in self.visit_ids:
            print(rec_visit.visit_date);
            for rec_diagnosis in rec_visit.diagnosis_id:
                print(rec_diagnosis.disease_id.name);
                if rec_diagnosis.disease_id == disease_id:
                    return f'{rec_visit.visit_date} {rec_diagnosis.doctor_id.name}'
        return ''

    #find visit with diagnosis of this disease
    def get_last_doctor_visit_date(self, doctor_id):
        self.ensure_one()
        for rec_visit in self.visit_ids:
            if rec_visit == doctor_id:
                return self.visit_ids.visit_date
        return ''


#        return f'{self.first_name} {self.family_name}'