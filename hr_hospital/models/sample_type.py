from odoo import models, fields, api


class HrHospitalSampleType(models.Model):
    _name = "hr_hospital.sample.type"
    _description = "Sample Type"
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(required=True)
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name', recursive=True,
        store=True)
    parent_id = fields.Many2one('hr_hospital.sample.type',
                                'Parent Type',
                                index=True,
                                ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many('hr_hospital.sample.type',
                               'parent_id', 'Child Type')
    sample_ids = fields.One2many('hr_hospital.sample',
                                 string='Sample',
                                 inverse_name='sample_type_id')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % \
                                         (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    def name_get(self):
        if not self.env.context.get('hierarchical_naming', True):
            return [(record.id, record.name) for record in self]
        return super().name_get()