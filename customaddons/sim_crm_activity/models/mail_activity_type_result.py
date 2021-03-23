from odoo import fields, models, api


class MailActivityTypeResult(models.Model):
    _name = 'mail.activity.type.result'
    _description = 'Description'

    name = fields.Char('Name')
    crm_stage_id = fields.Many2one('crm.stage', 'Stage')
    next_activity_type_id = fields.Many2one('mail.activity.type', 'Next activity type')
    activity_type_id = fields.Many2one('mail.activity.type', 'Activity type')
    next_activity_deadline = fields.Integer('Delay days')
