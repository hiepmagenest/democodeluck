# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pymessenger import Bot
import requests
import json
import datetime
from odoo.exceptions import ValidationError


class LiveVideos(models.Model):
    _name = 'live.videos'
    _rec_name = 'live_video_id'

    video_title = fields.Char(string=_("Title"))

    live_video_id = fields.Char(string=_("Video ID"))
    video_url = fields.Char(string=_("Stream URL"))
    secure_video_url = fields.Char(string=_("Secure Stream URL"))
    embed_html = fields.Char(string=_("Embed Html"))

    page_id = fields.Many2one('facebook.page')
    comment_ids = fields.One2many('facebook.comment', 'video_id')

    description_sended_comment = fields.Text()

    # Chua ro co status dung khong
    video_status = fields.Selection(string=_('Status'), selection=[
        ('none', 'NONE'),
        ('LIVE', 'LIVE'),
        ('VOD', 'VOD'),
        ('other', 'Other'),
    ], default='none')

    leads_count = fields.Integer(default=0, compute='_compute_count_facebook_leads')

    def _compute_count_facebook_leads(self):
        for rec in self:
            res = rec.env['crm.lead'].search([('live_video', '=', rec.id)])
            rec.leads_count = len(res)

    def action_show_lead(self):
        self.ensure_one()
        return {
            'name': ('Facebook Leads '),
            'view_mode': 'tree,form',
            'res_model': 'crm.lead',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('live_video', '=', self.id)],
            'target': 'current',
        }

    def fetch_comments_in_live_video(self):
        video_id = self.live_video_id
        access_token = self.page_id.page_access_token
        try:
            if video_id and access_token:
                request_url = "https://graph.facebook.com/v9.0/" + str(video_id) + \
                              "/comments?access_token=" + access_token
                req = requests.get(request_url)
                if req.status_code >= 200 and req.status_code < 300:
                    req.raise_for_status()
                    content = req.json()
                    if content:
                        for rec in content['data']:
                            commnet_id = self.env['facebook.comment'].search([('comment_id', '=', rec['id'])])
                            if not commnet_id:
                                created_time = datetime.datetime.strptime(rec['created_time'], '%Y-%m-%dT%H:%M:%S+0000')

                                # them moi comment vao live.videos
                                if 'from' in rec:
                                    user_id = rec['from']['id']
                                    fb_user = self.env['res.partner'].search([('fb_message_id', '=', user_id)])

                                    # them moi comment co san account ( facebook_user )
                                    if fb_user:
                                        new_comment = self.env['facebook.comment'].create({
                                            'message': rec['message'],
                                            'comment_id': rec['id'],
                                            'created_time': created_time,

                                            'video_id': self.id,
                                            'user_id': fb_user.id,
                                            'page_id': self.page_id.id,
                                        })
                                    else:
                                        # Tao moi user

                                        new_contact = self.env['res.partner'].create({
                                            "name": rec['from']['name'],
                                            "fb_message_id": rec['from']['id']
                                        })
                                        # Tao moi comment
                                        new_comment = self.env['facebook.comment'].create({
                                            'message': rec['message'],
                                            'comment_id': rec['id'],
                                            'created_time': created_time,

                                            'video_id': self.id,
                                            'user_id': new_contact.id,
                                            'page_id': self.page_id.id,

                                        })
                                # them moi comment khong co thong tin user fb
                                else:
                                    new_comment = self.env['facebook.comment'].create({
                                        'message': rec['message'],
                                        'comment_id': rec['id'],
                                        'video_id': self.id,
                                        'page_id': self.page_id.id,
                                        'created_time': created_time,
                                    })
                            # Update noi dung message khi fetch
                            else:
                                commnet_id.update({
                                    'message': rec['message'],
                                })
                        # Delete empty record
                        empty_records = self.env['facebook.comment'].sudo().search([('comment_id', '=', False)])
                        if empty_records:
                            empty_records.unlink()
                        # notification susscess
                        return {
                            'type': 'ir.actions.client',
                            'tag': 'reload',
                        }
                else:
                    # Neu respose != 200 , Thong bao ket noi that bai
                    error_msg = " Client Response " + str(req.status_code)
                    raise ValidationError(error_msg)
        except error as e:
            raise ValidationError(_('Error connection'))

    def create_lead(self):
        if self.comment_ids:
            list = []
            for rec in self.comment_ids:
                if rec.user_id not in list:
                    if rec.user_id:
                        list.append(rec.user_id)
            # Create new crm.lead
            if list:
                for rec in list:
                    # Checking duplicate record in crm.lead
                    fb_crm = self.env['crm.lead'].search([('live_video', '=', self.id), ('name', '=', rec.name)])

                    if not fb_crm:
                        new_crm_lead = self.env['crm.lead'].create({
                            'name': rec.name,
                            'live_video': self.id,
                            'partner_id': rec.id
                        })
                    else:
                        print("Duplicate record crm.lead")

    def reply_comment(self):
        access_token_page = self.page_id.page_access_token
        list_user_in_live_video = []
        bot = Bot(access_token_page, api_version="6.0")
        reponse_text = ""
        try:
            for rec in self.comment_ids:
                if rec.user_id not in list_user_in_live_video:
                    if rec.user_id.fb_message_id != False:
                        list_user_in_live_video.append(rec.user_id)

            if list_user_in_live_video:
                for user in list_user_in_live_video:
                    res = bot.send_text_message(user.fb_message_id, "Chao mung ban den voi " + self.page_id.page_name)
                    if res:
                        if 'error' in res:
                            reponse_text += "user :" + user.name + "\n"
                            reponse_text += res['error']['message'] + "\n\n"
            self.description_sended_comment = reponse_text
        except ValueError as e:
            raise ValidationError(_('Error connection '))

    def reply_comment_id(self):
        access_token_page = self.page_id.page_access_token
        page_id = self.page_id.page_id
        list_user = []
        reponse_text = ""
        try:
            # list user in live.video
            for rec in self.comment_ids:
                if rec.user_id not in list_user:
                    # if rec.user_id.name != False:
                    list_user.append(rec.user_id)
            print('list_user', list_user)
            # Send message to Customer using reply comment_id
            if page_id and access_token_page:
                if list_user:
                    for rec in list_user:
                        rec_comment_id = self.env['facebook.comment'].search([('user_id', '=', rec.id),
                                                                              ('video_id', '=', self.id),
                                                                              ('repply_comment', '=', False)],
                                                                             limit=1)
                        if rec_comment_id:
                            url = "https://graph.facebook.com/v9.0/" + page_id + "/messages?access_token=" + access_token_page
                            headers = {
                                'Content-type': 'application/json',
                            }
                            data = {
                                "messaging_type": "UPDATE",
                                "recipient": {
                                    "comment_id": rec_comment_id.comment_id
                                },
                                "notification_type": "REGULAR",
                                "message": {
                                    "text": "Chào mừng bạn đến với page" + self.page_id.page_name
                                }
                            }
                            response = requests.post(url, data=json.dumps(data), headers=headers)
                            if response.status_code == 200:
                                rec_comment_id.repply_comment = True
                            print("status :", response.status_code, "\n", response.text)
        except e:
            raise ValidationError(e)
