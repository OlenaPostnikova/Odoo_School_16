# -*- coding: utf-8 -*-
# from odoo import http


# class HpHospital(http.Controller):
#     @http.route('/hp_hospital/hp_hospital', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hp_hospital/hp_hospital/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hp_hospital.listing', {
#             'root': '/hp_hospital/hp_hospital',
#             'objects': http.request.env['hp_hospital.hp_hospital'].search([]),
#         })

#     @http.route('/hp_hospital/hp_hospital/objects/<model("hp_hospital.hp_hospital"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hp_hospital.object', {
#             'object': obj
#         })
