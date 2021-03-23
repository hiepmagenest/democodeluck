from odoo import models, fields, api, _


class ContactsFB(models.Model):
    _inherit = 'res.partner'

    fb_message_id = fields.Char(string=_("Facebook Message ID"))
    comment_count = fields.Integer(string=_("Comment count"), default=0, compute='_compute_count_comment_user')
    page_comment = fields.Many2one("facebook.page", string=_("Page Live Stream"))

    def _compute_count_comment_user(self):
        for rec in self:
            res = rec.env['facebook.comment'].search([('user_id', '=', rec.id)])
            rec.comment_count = len(res)

    def action_show_comment(self):
        self.ensure_one()
        return {
            'name': ('Comments'),
            'view_mode': 'tree,form',
            'res_model': 'facebook.comment',
            'type': 'ir.actions.act_window',
            'context': {'create': False, 'delete': False},
            'domain': [('user_id', '=', self.id)],
            'target': 'current',
        }

    # loi chua the su dung
    # def _open_all_view_facebook_contacts(self):
    #     action = self.env.ref('contacts.action_contacts').id
    #     action['domain'] = [('fb_message_id', '!=', False)]
    #     return action
