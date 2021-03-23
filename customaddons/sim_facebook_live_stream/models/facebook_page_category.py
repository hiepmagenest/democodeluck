# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class FacebookPageCategory(models.Model):
    _name = 'facebook.page.category'
    _rec_name = 'category_name'

    category_name = fields.Char(string=_("Category"))