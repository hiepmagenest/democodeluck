from odoo import fields, models, api, _


class CrmLeadAssignationSetting(models.Model):
    _name = 'crm.lead.assignation.setting'
    _description = 'Lead auto assign setting'
    _rec_name = 'name'

    name = fields.Char(string=_("Setting"), default="Setting")
    auto_setup_lead = fields.Boolean(string=_("Auto Assigned Lead"))

    withdraw_after = fields.Integer(string=_("Withdraw Lead After (minutes)"), default=60)

    lead_assignation_line_ids = fields.One2many('crm.lead.assignation.line', 'lead_assignation_setting')

    def action_open_view_from(self):
        rec_exist = self.env['crm.lead.assignation.setting'].sudo().search(
            [], limit=1)
        if rec_exist:
            res_id = rec_exist.id
        else:
            record = self.env['crm.lead.assignation.setting'].sudo().create(
                {
                    'name': "Setting",
                    'withdraw_after': 120
                })
            if record:
                res_id = record.id
        return {
            'name': 'Setting',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'current',
            'res_id': res_id,
            'res_model': 'crm.lead.assignation.setting',
        }
