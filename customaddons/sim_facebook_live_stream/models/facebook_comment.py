# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime


class FacebookComment(models.Model):
    _name = 'facebook.comment'
    _rec_name = 'message'
    _order = 'created_time ASC'  # DESC

    video_id = fields.Many2one('live.videos', string=_("Link Videos"))
    message = fields.Text("Message")
    comment_id = fields.Char("Comment ID")

    user_id = fields.Many2one("res.partner", string=_("User Comment"))
    page_id = fields.Many2one('facebook.page', related='video_id.page_id', )
    created_time = fields.Datetime(string=_("Created Time"))

    repply_comment = fields.Boolean(string=_("Reply Status"), default=False)

# def test_comment(self):
#     date_string = "2021-02-08T03:14:30+0000"
#     self.created_time = datetime.datetime.strptime(date_string,'%Y-%m-%dT%H:%M:%S+0000')
