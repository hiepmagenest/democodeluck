from odoo import models, fields, api, _


class CrmFB(models.Model):
    _inherit = 'crm.lead'

    live_video = fields.Many2one('live.videos', string=_("Live Video"))
    comment_ids = fields.One2many('facebook.comment', 'video_id', compute='_compute_filter_comment_user')

    def _compute_filter_comment_user(self):
        for rec in self:
            rec.comment_ids = False
            if rec.partner_id and rec.live_video:
                video_id = rec.live_video.id
                user_id = rec.partner_id.id
                comment_by_user = rec.env['facebook.comment'].search(
                    [('video_id', '=', video_id), ('user_id', '=', user_id)])
                if comment_by_user:
                    rec.comment_ids = comment_by_user
