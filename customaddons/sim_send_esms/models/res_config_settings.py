from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _descripion = 'Send SMS'

    sms_api_key = fields.Char(string="Api Key")
    sms_secret_Key = fields.Char(string="Secret Key")
    sms_type = fields.Char(string="SMS Type")
    sms_is_unicode = fields.Char(string="Unicode")
    sms_content = fields.Char(string="Content")
    sms_brandname = fields.Char(string="Brand Name")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['sms_api_key'] = self.env['ir.config_parameter'].sudo().get_param('sim_send_esms.sms_api_key')
        res['sms_secret_Key'] = self.env['ir.config_parameter'].sudo().get_param('sim_send_esms.sms_secret_Key')
        res['sms_type'] = self.env['ir.config_parameter'].sudo().get_param('sim_send_esms.sms_type')
        res['sms_is_unicode'] = self.env['ir.config_parameter'].sudo().get_param('sim_send_esms.sms_is_unicode')
        res['sms_content'] = self.env['ir.config_parameter'].sudo().get_param('sim_send_esms.sms_content')
        res['sms_brandname'] = self.env['ir.config_parameter'].sudo().get_param('sim_send_esms.sms_brandname')
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('sim_send_esms.sms_api_key', self.sms_api_key)
        self.env['ir.config_parameter'].sudo().set_param('sim_send_esms.sms_secret_Key', self.sms_secret_Key)
        self.env['ir.config_parameter'].sudo().set_param('sim_send_esms.sms_type', self.sms_type)
        self.env['ir.config_parameter'].sudo().set_param('sim_send_esms.sms_is_unicode', self.sms_is_unicode)
        self.env['ir.config_parameter'].sudo().set_param('sim_send_esms.sms_content', self.sms_content)
        self.env['ir.config_parameter'].sudo().set_param('sim_send_esms.sms_brandname', self.sms_brandname)
        super(ResConfigSettings, self).set_values()
