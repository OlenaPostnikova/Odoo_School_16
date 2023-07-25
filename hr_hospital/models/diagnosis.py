from odoo import models, fields, api

class HrHospitalDiagnosis(models.Model):
    _name = 'hr_hospital.diagnosis'
    _description = 'Hospital patient diagnosises'

    name = fields.Char(required=True)
    active = fields.Boolean(
        default=True, )

    diagnosis_date = fields.Date('Diagnosis date')
    patient_id = fields.Many2one(comodel_name='hr_hospital.patient', string='Patient')
    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor', string='Doctor')
    disease_id = fields.Many2one(comodel_name='hr_hospital.disease', string='Disease')
    recommendation = fields.Text()

    comment = fields.Char(required=False,
                          states={'mentor comment is required': [('required', True)]})
    # mentor comment is required
    state = fields.Char(compute='_compute_state')
    qty = fields.Integer(default=1, )

    @api.depends('doctor_id')
    def _compute_state(self):
        for rec in self:
            if rec.doctor_id.is_intern:
                rec.state = 'mentor comment is required'
            else:
                rec.state = 'mentor comment is not required'

    def get_diagnosis_(self, patient_id, doctor_id, disease_id):
        for rec in self:
            for rec_patients in self.patient_id:
                if rec.doctor_id == doctor_id and rec.disease_id == disease_id:
                    return self.visit_ids.visit_date
            return ''