from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class HrHospitalVisit(models.Model):
    _name = 'hr_hospital.visit'
    _description = "Hospital appointment"

    name = fields.Char()
    active = fields.Boolean(
        default=True, )
    is_done = fields.Boolean()
    visit_date = fields.Datetime('Date', readonly=False,
                                 states={'appointment has been done': [('readonly', True)]})
    # don't change if visit has been done
    state = fields.Char(compute='_compute_state')
    patient_id = fields.Many2one('hr_hospital.patient', string='Patient')
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor')
    # don't delete if diagnosis exists
    diagnosis_id = fields.Many2one('hr_hospital.diagnosis', string='Diagnose')
    state_not_delete = fields.Char(compute='_compute_state_not_delete')

    recommendation = fields.Text()
    comment = fields.Char()

    # method depends - automatic changing one field with an other
    @api.depends('is_done')
    def _compute_state(self):
        for rec in self:
            if rec.is_done:
                rec.state = 'appointment has been done'
            else:
                rec.state = 'appointment has not been done'

    @api.depends('diagnosis_id')
    def _compute_state_not_delete(self):
        for rec in self:
            if rec.diagnosis_id:
                rec.state_not_delete = True
            else:
                rec.state_not_delete = False

    # to prohibit changing visit_date
    # method onchange
    @api.onchange('visit_date')
    def _check_visit_date_(self):
        for rec in self:
            if rec.diagnosis_id:
                rec.state_not_delete = True
            else:
                rec.state_not_delete = False

    # 1.check that doctor not allowed to have 2 appointments on the same time
    # method constrains
    @api.constrains('doctor_id', 'visit_date')
    def check_doctor_time(self):

        for rec in self:
            result = self.search([
                ('doctor_id', '=', rec.doctor_id.id),
                ('visit_date', '=', rec.visit_date),
                ('id', '!=', rec.id)
            ])

            if result:
                raise (
                    ValidationError(
                        'Time ' + str(rec.visit_date) + ' for doctor ' + rec.doctor_id.name + 'is already used')
                )

    # 2.check that patient not allowed to have 2 appointments on the same time
    @api.constrains('patient_id', 'visit_date')
    def check_patient_time(self):
        for rec in self:
            result = self.search([
                ('patient_id', '=', rec.patient_id.id),
                ('visit_date', '=', rec.visit_date),
                ('id', '!=', rec.id)
            ])

            if result:
                raise (
                    ValidationError(
                        'Time ' + str(rec.visit_date) + ' for patient' + rec.patient_id.name + 'is already used')
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_only_if_open(self):
        for statement in self:
            if statement.diagnosis_id:
                raise UserError(
                    'Not allowed to delete visit '
                    'You need to clear diagnosis')
