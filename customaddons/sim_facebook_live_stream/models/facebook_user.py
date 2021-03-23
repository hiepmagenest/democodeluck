# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class FacebookUser(models.Model):
    _name = 'facebook.user'
    _rec_name = 'fb_name'

    fb_name = fields.Char(string=_("Facebook Name"))
    fb_id = fields.Char(string=_("Facebook ID"))
