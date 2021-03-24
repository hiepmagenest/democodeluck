# -*- coding: utf-8 -*-
from odoo import fields, models


# Part of Kanak Infosystems LLP. See LICENSE file for full copyright and licensing details.


class ResCompany(models.Model):
    _inherit = 'res.company'

    purchase_order_approval_rule_id = fields.Many2one('purchase.order.approval.rule',
                                                      string='Purchase Order Approval Rules')
    purchase_order_approval = fields.Boolean(string='Purchase Order Approval By Rule')
