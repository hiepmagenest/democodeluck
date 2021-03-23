# -*- coding: utf-8 -*-
# from odoo import http


# class SimCrmActivity(http.Controller):
#     @http.route('/sim_crm_activity/sim_crm_activity/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sim_crm_activity/sim_crm_activity/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sim_crm_activity.listing', {
#             'root': '/sim_crm_activity/sim_crm_activity',
#             'objects': http.request.env['sim_crm_activity.sim_crm_activity'].search([]),
#         })

#     @http.route('/sim_crm_activity/sim_crm_activity/objects/<model("sim_crm_activity.sim_crm_activity"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sim_crm_activity.object', {
#             'object': obj
#         })
