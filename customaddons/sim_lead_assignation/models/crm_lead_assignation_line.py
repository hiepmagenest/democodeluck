from odoo import fields, models, api, _


class CrmLeadAssignationLine(models.Model):
    _name = 'crm.lead.assignation.line'
    _description = 'Lead auto assign line'

    lead_assignation_id = fields.Many2one('crm.lead.assignation')
    lead_assignation_setting = fields.Many2one('crm.lead.assignation.setting')

    sequence = fields.Integer(required=True, string=_("Sequence"), default=10)

    campaign_id = fields.Many2one('utm.campaign', string=_("Campaign"))
    source_id = fields.Many2one('utm.source', string=_("Source"))
    tag_id = fields.Many2one('crm.tag', string=_("Tag"))

    date_from = fields.Date(string=_("Date From")) # Chua su dung
    date_to = fields.Date(string=_("Date To"))   # Chua su dung

    user_ids = fields.Many2many('res.users', string=_("Sale User"))
    team_id = fields.Many2one('crm.team', string=_("Sale Team"))
