from odoo import _, models, fields

class NewDoctorWizard(models.TransientModel):
    _name = 'new.doctor.wizard'
    _description = 'Change personal doctor for all patients'


    def default_patient(self):
        return self.env['hr_hospital.patient'].browse(self._context.get('active_ids'))

    patient_ids = fields.Many2many('hr_hospital.patient',
                                   string='Patients',
                                   default=default_patient)
    doctor_id = fields.Many2one('hr_hospital.doctor', string='Doctor')

#not used yet
    def action_open_wizard(self):
        return {
            'name':_('Change current doctor for all patients'),
            'type':'ir.action.act_window',
            'view_mode':'form',
            'res_model':'new.doctor.wizard',
            'target':'new',
            'context':{'default_doctor_id': self.env['hr_hospital.doctor'].browse(self._context.get('active_ids'))},
        }
# not used yet

    def action_set_new_doctor(self):
        for record in self.patient_ids:
            record.doctor_id = self.doctor_id