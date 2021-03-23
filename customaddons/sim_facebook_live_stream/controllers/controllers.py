# -*- coding: utf-8 -*-
# from odoo import http


# class MagenestFacebookLiveStream(http.Controller):
#     @http.route('/sim_facebook_live_stream/sim_facebook_live_stream/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sim_facebook_live_stream/sim_facebook_live_stream/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sim_facebook_live_stream.listing', {
#             'root': '/sim_facebook_live_stream/sim_facebook_live_stream',
#             'objects': http.request.env['sim_facebook_live_stream.sim_facebook_live_stream'].search([]),
#         })

#     @http.route('/sim_facebook_live_stream/sim_facebook_live_stream/objects/<model("sim_facebook_live_stream.sim_facebook_live_stream"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sim_facebook_live_stream.object', {
#             'object': obj
#         })
