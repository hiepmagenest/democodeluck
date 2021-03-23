# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json


class SimSendEsms(models.Model):
    _inherit = 'crm.lead'

    phone_inherit = fields.Char(string="Phone")

    def send_sms_api(self):
        sms_api_key = self.env['ir.config_parameter'].sudo().get_param('sim_send_esms.sms_api_key')
        sms_secret_Key = self.env['ir.config_parameter'].sudo().get_param(
            'sim_send_esms.sms_secret_Key')
        sms_type = self.env['ir.config_parameter'].sudo().get_param('sim_send_esms.sms_type')
        sms_is_unicode = self.env['ir.config_parameter'].sudo().get_param(
            'sim_send_esms.sms_is_unicode')
        sms_content = self.env['ir.config_parameter'].sudo().get_param('sim_send_esms.sms_content')
        sms_brandname = self.env['ir.config_parameter'].sudo().get_param('sim_send_esms.sms_brandname')
        url = "http://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_post_json/"
        headers = {
            'Content-Type': 'application/json',
        }

        payload = {
            "ApiKey": sms_api_key,
            "Content": sms_content,
            "Phone": self.phone_inherit,
            "SecretKey": sms_secret_Key,
            "IsUnicode": sms_is_unicode,
            "Brandname": sms_brandname,
            "SmsType": sms_type
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        print(response.text)
