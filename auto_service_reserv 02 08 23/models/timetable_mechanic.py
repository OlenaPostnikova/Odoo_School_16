from odoo import models, fields, api


class AutoServiceTimeTableMechanic(models.Model):
    _name = 'auto_service.timetable_mechanic'
    _description = 'Auto service mechanics time table'

    active = fields.Boolean(
        default=True, )
    name = fields.Char()
    mechanic_id = fields.Many2one('auto_service.mechanic')
    date = fields.Date(string='Date')
    # для расчетов
    start_time_int = fields.Integer(string='Hours from')
    end_time_int = fields.Integer(string='Hours to')
    # для хранения в расписании
    start_time = fields.Datetime(string='From')
    end_time = fields.Datetime(string='To')

    @api.onchange('mechanic_id', 'start_time', 'end_time')
    def _compute_name(self):
        # для отображения
        for trace in self:
            trace.name = '%s: %s - %s' % (trace.mechanic_id.name, trace.start_time_int, trace.end_time_int)

