# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LiveStream(models.Model):
    _name = 'live.stream'
    # # _rec_name = 'stream_title'
    #
    # stream_title = fields.Char("Title")
    #
    #
    # status_live = fields.Selection({
    #     'live_now': 'LIVE_NOW',
    #     'unpublished': 'UNPUBLISHED',
    #     'scheduled_unpublished': 'SCHEDULED_UNPUBLISHED',
    #     'scheduled_live': 'SCHEDULED_LIVE',
    # })
