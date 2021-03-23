# -*- coding: utf-8 -*-
# from odoo import http


# class SimLeadAssignation(http.Controller):
#     @http.route('/sim_lead_assignation/sim_lead_assignation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sim_lead_assignation/sim_lead_assignation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sim_lead_assignation.listing', {
#             'root': '/sim_lead_assignation/sim_lead_assignation',
#             'objects': http.request.env['sim_lead_assignation.sim_lead_assignation'].search([]),
#         })

#     @http.route('/sim_lead_assignation/sim_lead_assignation/objects/<model("sim_lead_assignation.sim_lead_assignation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sim_lead_assignation.object', {
#             'object': obj
#         })
