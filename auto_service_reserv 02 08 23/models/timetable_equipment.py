from odoo import models, fields, api

class AutoServiceTimeTableEquipment(models.Model):
    _name = 'auto_service.timetable_equipment'
    _description = 'Auto service mechanics time table'

    active = fields.Boolean(
        default=True, )
    name = fields.Char()
    equipment_id = fields.Many2one('auto_service.equipment')
    date = fields.Date(string='Date')
    start_time = fields.Datetime(string='From')
    end_time = fields.Datetime(string='To')
    @api.onchange('equipment_id', 'start_time', 'end_time')
    def _compute_name(self):
        for trace in self:
            trace.name = '%s: %s - %s' % (trace.equipment_id.name, trace.start_time, trace.end_time)

