# -*- coding: utf-8 -*-
# Part of Kanak Infosystems LLP. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ApprovalRole(models.Model):
    _name = 'approval.role'
    _description = 'Approval Role'

    name = fields.Char(required=True)


class ApprovalCategory(models.Model):
    _name = 'purchase.approval.category'
    _description = 'Approval Category'

    name = fields.Char(required=True)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'HR Employee'

    approval_role = fields.Many2many('approval.role', 'approval_role_hr_employee_rel', 'approval_role_id',
                                     'hr_employee_id', string='Approval Role')


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    approval_category = fields.Many2one('purchase.approval.category', string='Approval Category')
