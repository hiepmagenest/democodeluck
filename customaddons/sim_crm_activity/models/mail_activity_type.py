from odoo import fields, models, api

class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    activity_type_result_ids = fields.One2many('mail.activity.type.result', 'activity_type_id', 'Result')
    activity_type_crm_lead_bool = fields.Boolean('',compute='compute_activity_type_crm_lead_bool')

    def compute_activity_type_crm_lead_bool(self):
        for rec in self:
            rec.activity_type_crm_lead_bool = False
            if rec.sudo().res_model_id:
                if rec.sudo().res_model_id.model == 'crm.lead':
                    rec.activity_type_crm_lead_bool = True
