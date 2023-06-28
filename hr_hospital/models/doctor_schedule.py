from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class HrHospitalDoctorSchedule(models.Model):
    _name = 'hr_hospital.doctor.schedule'
    _description = 'Hospital doctors schedule'

    active = fields.Boolean(
        default=True, )
    doctor_id = fields.Many2one('hr_hospital.doctor')
    date = fields.Date('Date')
    begin_time = fields.Datetime('From', readonly=False)
    end_time = fields.Datetime('To', readonly=False)

    # @api.constrains('doctor_id','date','begin_time','end_time')
    # def check_time(self):
    #
    #     for rec in self:
    #           result = self.search([
    #             ('doctor_id', '=' , rec.doctor_id.id),
    #             ('date', '=',  rec.date)
    #           ])
    #
    #           for recf in result:
    #               if rec.begin_time >= recf.begin_time and rec.begin_time <= recf.end_time:
    #                 raise (
    #                       ValidationError('Time from ' + str(recf.begin_time) + ' to ' + str(recf.end_time) + ' is already used')
    #                 )
    #
    #               if rec.end_time >= recf.begin_time and rec.end_time <= recf.end_time:
    #                   raise (
    #                       ValidationError('Time from ' + str(recf.begin_time) + ' to ' + str(recf.end_time) + ' is already used')
    #                   )




