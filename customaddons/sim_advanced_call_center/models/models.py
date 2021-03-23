# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    # call id for api
    call_id = fields.Char('Call ID', )


class CallEffect(models.TransientModel):
    _name = 'call.effect'

    name = fields.Char()
    phone = fields.Char()
    customer = fields.Char(string='Customer')
    has_customer = fields.Boolean(default=False)
    description = fields.Html(string='Information', sanitize_attributes=False, readonly=True)

    # permission = fields.Boolean('Permission', compute='_check_permission_user')

    def on_create_lead(self):
        ir_model_data = self.env['ir.model.data']
        # form_view = \
        #     ir_model_data.get_object_reference('sim_advanced_crm', 'lead_form_view')[1]
        content_name = ""
        if self.env.user.lang == "vi_VN":
            content_name = "Tạo tiềm năng"
        else:
            content_name = "Create Lead"
        return {
            'name': content_name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'crm.lead',
            'target': 'current',
            # 'views': [(form_view, 'form'), ],
            'context': {
                'default_phone': self.phone,
                'default_type': 'lead'
            }
        }
    # def _check_permission_user(self):
    #     for rec in self:
    #         user = self.env['hr.employee'].sudo().browse(rec._uid)
    #         # check is user tong dai/marketing
    #         operator = self.env['res.groups'].sudo().search([('name','=','DEMO Switch Operator Access (Tổng đài)')])
    #         marketing = self.env['res.groups'].sudo().search([('name','=','DEMO Marketing Access')])
    #         if user in operator.users or user in marketing.users:
    #             rec.permission = True
    #         else:
    #             rec.permission = False
