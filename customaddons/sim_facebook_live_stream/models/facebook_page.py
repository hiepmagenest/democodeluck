# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
import json
from odoo.exceptions import ValidationError


class FacebookPage(models.Model):
    _name = 'facebook.page'
    _rec_name = 'page_name'
    page_name = fields.Char(string=_("Name"))
    page_id = fields.Char(string=_("Page ID"))
    page_url = fields.Char(string=_("URL"))
    page_access_token = fields.Text(string=_("PAGE ACCESS TOKEN"))
    page_category = fields.Many2one(string=_('facebook.page.category'))

    page_status = fields.Selection(string=_('Status'), selection=[
        ('none', 'NONE'),
        ('live_now', 'LIVE_NOW'),
        ('shutdown', 'SHUTDOWN')
    ], default='none')

    live_video_count = fields.Integer(default=0, compute='_compute_count_live_videos')

    def _compute_count_live_videos(self):
        for rec in self:
            res = rec.env['live.videos'].search([('page_id', '=', rec.id)])
            rec.live_video_count = len(res)

    def action_show_live_video(self):
        self.ensure_one()
        return {
            'name': ('Live Videos'),
            'view_mode': 'tree,form',
            'res_model': 'live.videos',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('page_id', '=', self.id)],
            'target': 'current',
        }

    def fetch_live_videos(self):
        page_id = self.page_id
        fb_token = self.page_access_token
        list_option = ['none', 'LIVE', 'VOD', 'other']
        try:
            if page_id and fb_token:
                request_url = "https://graph.facebook.com/v9.0/" + str(
                    page_id) + "/" + "live_videos?access_token=" + str(fb_token)
                req = requests.get(request_url)

                # Kiem tra response 200 thuc hien cap nhap thong tin video
                if req.status_code >= 200 and req.status_code < 300:
                    content = req.json()
                    if content:
                        for rec in content['data']:
                            video = self.env['live.videos'].search([('live_video_id', '=', rec['id'])], limit=1)
                            # Cap nhap record live.video da ton tai trong database
                            if video:
                                # check status co trong rec hay khong
                                if 'status' in rec:
                                    # check gia tri status tra ve co nam trong nhung option da biet hay khong
                                    # neu khong thi set gia tri la other
                                    if rec['status'] in list_option:
                                        video.update({
                                            'video_status': rec['status'],
                                        })
                                    else:
                                        video.update({
                                            'video_status': 'other',
                                        })
                                if 'title' in rec:
                                    video.update({
                                        'video_title': rec['title'],
                                    })
                            # Tao moi record live.video
                            else:
                                new_video = self.env['live.videos'].create({

                                    'live_video_id': rec['id'],

                                    'video_url': rec['stream_url'],
                                    'secure_video_url': rec['secure_stream_url'],
                                    'embed_html': rec['embed_html'],
                                    'page_id': self.id,
                                })
                                if 'title' in rec:
                                    new_video.update({
                                        'video_title': rec['title']
                                    })
                                if rec['status'] in list_option:
                                    new_video.update({
                                        'video_status': rec['status']
                                    })
                                else:
                                    new_video.update({
                                        'video_status': 'other'
                                    })

                    return {
                        'type': 'ir.actions.client',
                        'tag': 'reload',
                    }
                else:
                    # Neu respose != 200 , Thong bao ket noi that bai
                    error_msg = "Client Response " + str(req.status_code)
                    raise ValidationError(error_msg)
        except ValueError as e:
            raise ValidationError(e)
