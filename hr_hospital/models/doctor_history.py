from odoo import models, fields


class HrHospitalDoctorHistory(models.Model):
    _name = 'hr_hospital.doctor.history'
    _description = "History of personal doctor"

    date = fields.Date('Date')
    patient_id = fields.Many2one('hr_hospital.patient')
    doctor_id = fields.Many2one('hr_hospital.doctor')