from odoo import models, fields
from datetime import timedelta


class ScheduleLineWizard(models.TransientModel):
    _name = 'schedule.line.wizard'
    _description = 'New schedule lines even & odd'

    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor')
    date = fields.Date('Date')
    week_number = fields.Integer('Week #')
    begin_time = fields.Datetime('From')
    end_time = fields.Datetime('To')


class NewScheduleWizard(models.TransientModel):
    _name = 'new.schedule.wizard'
    _description = 'Create new doctors schedule for even & odd weeks'

    doctor_id = fields.Many2one(comodel_name='hr_hospital.doctor',
                                string='Doctor',
                                required=True,
                                domain=[('is_intern', '=', False)])
    # to create schedule from start_date for weeks_amount weeks
    #start_date = fields.Date('Start date')
    start_date = fields.Datetime('Start date')
    weeks_amount = fields.Integer('Weeks amount')

    # one line of hr_hospital.doctor.schedule
    # even week------------------------
    begin_time_mon_even = fields.Integer(string='Monday (even) from')
    end_time_mon_even = fields.Integer(string='Monday (even) to')
    begin_time_tue_even = fields.Integer('Tuesday (even) from')
    end_time_tue_even = fields.Integer('Tuesday (even) to')
    # begin_time_wed_even = fields.Datetime('Wednesday from')
    # end_time_wed_even = fields.Datetime('To')
    # begin_time_thu_even = fields.Datetime('Thursday from')
    # end_time_thu_even = fields.Datetime('To')

    # odd week-----------------------------
    begin_time_mon_odd = fields.Integer('Monday (odd) from')
    end_time_mon_odd = fields.Integer('Monday (odd) to')
    begin_time_tue_odd = fields.Integer('Tuesday (odd) from')
    end_time_tue_odd = fields.Integer('Tuesday (odd) to')
    # begin_time_wed_odd = fields.Datetime('Wednesday from')
    # end_time_wed_odd = fields.Datetime('To')
    # begin_time_thu_odd = fields.Datetime('Thursday from')
    # end_time_thu_odd = fields.Datetime('To')

    # one line of schedule (day + time)
    schedule_line_ids = fields.Many2many('schedule.line.wizard')

    def _add_line(self, current_date):

        current_week = float(current_date.strftime("%W"))
        current_day = current_date.strftime("%a")

        if current_week / 2 == int(current_week / 2):
            # even week
            if current_day == "Mon" and self.begin_time_mon_even:
                self._add_line_structure(current_date, self.begin_time_mon_even, self.end_time_mon_even)
            elif current_day == "Tue" and self.begin_time_tue_even:
                self._add_line_structure(current_date, self.begin_time_tue_even, self.end_time_tue_even)
        else:
            # odd week
            if current_day == "Mon" and self.begin_time_mon_odd:
                self._add_line_structure(current_date, self.begin_time_mon_odd, self.end_time_mon_odd)
            elif current_day == "Tue" and self.begin_time_tue_odd:
                self._add_line_structure(current_date, self.begin_time_tue_odd, self.end_time_tue_odd)

    def _add_line_structure(self, current_date, begin_time, end_time):

        print(current_date.strftime("%d-%m-%y %H:%M"))
        #date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

        print(begin_time)
        print(end_time)
        begin_time = current_date + timedelta(seconds=begin_time*60*60)
        end_time = current_date + timedelta(seconds=end_time*60*60)
        print(begin_time.strftime("%d-%m-%y %H:%M"))
        print(end_time)

        for rec in self:
            new_line = {
                'date': current_date,
                'doctor_id': rec.doctor_id.id,
                'begin_time': begin_time,
                'end_time': end_time,
            }
            rec.schedule_line_ids.create(new_line)
            self.env['hr_hospital.doctor.schedule'].create(new_line)

    def action_create_lines(self):
        print('------------------------ action_create_lines ------------------- ')
        i = 1
        j = 1

        #date_time
        current_date = self.start_date
        print('----------------------------------------------------')
        print(self.start_date)
        print(current_date)

        # loop weeks
        while i <= self.weeks_amount:
            # loop days of week
            while j <= 7:
                print(current_date)
                self._add_line(current_date)
                current_date = current_date + timedelta(hours=24)
                j += 1
            i += 1

    def action_create(self):
        for rec in self:
            for line in self.schedule_line_ids:
                self.env['hr_hospital.doctor.schedule'].create({
                    'doctor_id': rec.doctor_id.id,
                    'date': rec.date,
                    'begin_time': line.begin_time,
                    'end_time': line.end_time,
                })
