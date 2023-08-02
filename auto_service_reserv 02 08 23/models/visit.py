from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class AutoServiceVisit(models.Model):
    _name = 'auto_service.visit'
    _description = "Car service visit"

    name = fields.Char()
    active = fields.Boolean(
        default=True, )

    visit_date = fields.Date('Date', readonly=False,
                             states={'visit has been done': [('readonly', True)]})
    start_time_int = fields.Integer('Time_int')
    start_time = fields.Datetime('Time_date')

    vehicle_id = fields.Many2one('auto_service.vehicle', string='Vehicle')
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    problem = fields.Char(string='Description of the problem(s)')
    car_mileage = fields.Integer(required=False, string='Car mileage')

    equipment_id = fields.Many2one('auto_service.equipment', string='Equipment required')
    mechanic_id = fields.Many2one('auto_service.mechanic', string='Mechanic')

    job_id = fields.Many2one('auto_service.job', string='Job')
    job_recommended_id = fields.Many2one('auto_service.job', string='Job recommended')
    duration = fields.Integer(required=False, default=1, string='Duration,hours')
    price = fields.Float(required=False, string='Price,£')

    is_done = fields.Boolean()
    recommendation = fields.Text(string='Recommendation')
    comment = fields.Char(string='Comment')

    state = fields.Char(compute='_compute_state')
    # state_not_delete = fields.Char(compute='_compute_state_not_delete')
    state_not_delete = fields.Char(compute='_compute_state')

    @api.onchange('vehicle_id')
    def _compute_mileage_customer(self):
        for rec in self:
            if rec.vehicle_id:
                rec.car_mileage = rec.vehicle_id.car_mileage
                rec.customer_id = rec.vehicle_id.customer_id

    @api.onchange('job_id')
    def _compute_equipment_onchange(self):
        for rec in self:
            if rec.job_id:
                rec.equipment_id = rec.job_id.equipment_id.id
                rec.duration = rec.job_id.duration
                rec.price = rec.job_id.price

    @api.ondelete(at_uninstall=False)
    def _unlink_only_if_open(self):
        for statement in self:
            if statement.is_done:
                raise UserError(
                    'Not allowed to delete appointment'
                    'Visit has been done')

    @api.depends('is_done')
    def _compute_state(self):
        for rec in self:
            if rec.is_done:
                rec.state = 'visit has been done'
                rec.state_not_delete = True
            else:
                rec.state = 'visit has not been done'
                rec.state_not_delete = False

    @api.onchange('visit_date')
    def _check_visit_date_(self):
        self._check_mechanic_timetable()
        self._check_mechanic_is_busy()
        # self._check_equipment_is_busy()
        self._check_vehicle_is_busy()

    @api.onchange('mechanic_id')
    def _check_visit_date_(self):
        self._check_mechanic_timetable()
        self._check_mechanic_is_busy()

    @api.onchange('job_id', 'equipment_id')
    def _check_visit_date_(self):
        self._check_equipment_timetable()
        # self._check_equipment_is_busy()
    # -------------------------------
    # Метод constrains отрабатывает при записи
    @api.constrains('visit_date', 'mechanic_id', 'equipment_id', 'vehicle_id')
    def check_visit(self):
        # перед записью проверяем:
        # 1 есть ли время по расписанию у механика,
        # 2 есть ли время по расписанию у оборудования
        # 3 нет ли у механика других визитов, занимающих это время
        # 4 не занято ли оборудование в это же время
        # 5 не записан ли этот автомобиль на это же время
        pass
        # self._check_mechanic_timetable()
        # self._check_equipment_timetable()
        # self._check_mechanic_is_busy()
        # # self._check_equipment_is_busy()
        # self._check_vehicle_is_busy()

    def _if_time_slots_cross(self, start1, end1, start2, end2):
        # функция проверяет, пересекаются ли слоты
        # Параметры: start1,end1 - интервал,который нужно установить в документе
        #           start2,end2 - интервал, который уже занят в этот день
        # если дата начала или дата конца, проверяемого интвервала, попадает в середину другого, значит, пересекаются
        if (start1 >= start2 and start1 <= end1) or (end1 >= start1 and end1 <= end2):
            return True
        else:
            return False

    def _check_mechanic_timetable(self):
        # есть ли расписание у механика на это время
        for rec in self:
            result_search = rec.mechanic_id.timetable_ids.search([
                ('mechanic_id', '=', rec.mechanic_id.id),
                ('date', '=', rec.visit_date)
            ])
            for rec_search in result_search:
                if self._if_time_slots_cross(rec.start_time_int,
                                             rec.start_time_int + rec.duration,
                                             rec_search.start_time,
                                             rec_search.start_time + rec_search.duration):
                    return
            # время в расписании не найдено
            raise (ValidationError('' + rec.mechanic_id.name + ' : no timesheet at that time'))
    def _check_equipment_timetable(self):
        # не запланирован ли ремонт оборудования на это время, наоборот, ищем, чтоб не было записи
        for rec in self:
            result_search = rec.equipment_id.timetable_ids.search([
                ('equipment_id', '=', rec.equipment_id.id),
                ('date', '=', rec.visit_date)
            ])
            for rec_search in result_search:
                for rec_search in result_search:
                    if self._if_time_slots_cross(rec.start_time_int,
                                                 rec.start_time_int + rec.duration,
                                                 rec_search.start_time,
                                                 rec_search.start_time + rec_search.duration):
                        raise (ValidationError('' + rec.equipment_id.name + ' : no timesheet at that time'))

    def _check_mechanic_is_busy(self):
        # 3 нет ли у механика других визитов, занимающих это время
        for rec in self:
            result_search = self.search([
                ('mechanic_id', '=', rec.mechanic_id.id),
                ('visit_date', '=', rec.visit_date),
                ('id', '!=', rec.id)
            ])
            for rec_search in result_search:
                if self._if_time_slots_cross(rec.start_time_int,
                                             rec.start_time_int + rec.duration,
                                             rec_search.start_time,
                                             rec_search.start_time + rec_search.duration):
                    raise (ValidationError('' + rec.mechanic_id.name + ' : other visit at that time'))
    def _check_equipment_is_busy(self):
        # 4 не занято ли оборудование в это время
        return
        # for rec in self:
        #     result_search = self.search([
        #             ('equipment_id', '=', rec.equipment_id.id),
        #             ('visit_date', '=', rec.visit_date),
        #             ('id', '!=', rec.id)
        #                 ])
            # for rec_search in result_search:
            #     if self._if_time_slots_cross(rec.start_time_int,
            #                                  rec.start_time_int + rec.duration,
            #                                  rec_search.start_time,
            #                                  rec_search.start_time + rec_search.duration):
            #         raise (ValidationError('' + rec.equipment_id.name + ' : other visit at that time'))

    def _check_vehicle_is_busy(self):
        # 5 не записан ли этот автомобиль в другой визит на это же время
        for rec in self:
            result_search = self.search([
                ('vehicle_id', '=', rec.vehicle_id.id),
                ('visit_date', '=', rec.visit_date),
                ('id', '!=', rec.id)
            ])
            for rec_search in result_search:
                if self._if_time_slots_cross(rec.start_time_int,
                                             rec.start_time_int + rec.duration,
                                             rec_search.start_time,
                                             rec_search.start_time + rec_search.duration):
                    raise (ValidationError('' + rec.vehicle_id.name + ' : other visit at that time'))


