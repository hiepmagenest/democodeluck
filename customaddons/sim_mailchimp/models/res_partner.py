from odoo import fields, models, api, SUPERUSER_ID


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _compute_mailchimp_subscription_list_ids(self):
        for record in self:
            if record.email:
                query = """
                    SELECT rel.id
                        FROM mailing_contact mc
                        JOIN mailing_contact_list_rel rel
                        ON rel.contact_id = mc.id
                    WHERE 
                        LOWER(substring(email, '([^ ,;<@]+@[^> ,;]+)')) = LOWER(substring('{}', '([^ ,;<@]+@[^> ,;]+)'))
                        AND rel.mailchimp_list_id is not null""".format(record.email.replace("'", "''"))
                self._cr.execute(query)
                results = self._cr.fetchall()
                subscription_list_ids = []
                for result_tuple in results:
                    subscription_list_ids.append(result_tuple[0])
                record.subscription_list_ids = subscription_list_ids
            else:
                record.subscription_list_ids = False

    subscription_list_ids = fields.Many2many('mailing.contact.subscription',
                                             compute="_compute_mailchimp_subscription_list_ids",
                                             groups='mass_mailing.group_mass_mailing_user',
                                             string='Subscription Information')

    def action_export_partner_mailchimp(self, mailchimp_list_id):
        mailing_contact_obj = self.env['mailing.contact']
        partner_export_mailchimp_obj = self.env['partner.export.mailchimp']
        for partner_id in self:
            contact_id = partner_export_mailchimp_obj.get_mailing_contact_id(partner_id, force_create=True)
            if contact_id:
                contact_id = mailing_contact_obj.browse(contact_id)
                if mailchimp_list_id.id not in contact_id.subscription_list_ids.mapped('list_id').mapped(
                        'mailchimp_list_id').ids:
                    vals = {'list_id': mailchimp_list_id.odoo_list_id.id, 'contact_id': contact_id.id}
                    contact_id.subscription_list_ids.create(vals)
                    contact_id.action_export_to_mailchimp()
        return True

    def get_mailing_contact_to_update(self):
        self.ensure_one()
        partner_export_mailchimp_obj = self.env['partner.export.mailchimp']
        contact_id = partner_export_mailchimp_obj.get_mailing_contact_id(self)
        if contact_id:
            contact_id = self.env['mailing.contact'].browse(contact_id)
        return contact_id

    def write(self, vals):
        if 'email' in vals and not self._context.get('no_need'):
            for record in self.with_user(SUPERUSER_ID).filtered(lambda x: x.subscription_list_ids):
                contact_id = record.get_mailing_contact_to_update()
                contact_id.write({'email': vals.get('email')})
        res = super(ResPartner, self).write(vals)
        if not self._context.get('no_need'):
            for rec in self.with_user(SUPERUSER_ID):
                if rec.subscription_list_ids:
                    mapped_merge_fields = rec.subscription_list_ids.mapped('mailchimp_list_id').get_mapped_merge_field()
                    if any([merge_field in vals for merge_field in mapped_merge_fields]):
                        contact_id = rec.get_mailing_contact_to_update()
                        if contact_id:
                            contact_id.action_update_to_mailchimp()
        return res
