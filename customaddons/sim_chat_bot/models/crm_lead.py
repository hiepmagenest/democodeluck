# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    facebook_sender_id = fields.Char(string='Facebook Id', index=True)
