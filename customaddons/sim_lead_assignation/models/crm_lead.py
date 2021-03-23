from odoo import api, fields, models, _
from datetime import datetime


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def compute_crm_user_id(self):
        if self.env.user.has_group('sales_team.group_sale_salesman'):
            user_login = self.env.user.id
            return user_login
        return None

    user_id = fields.Many2one('res.users', string=_('Salesperson'), index=True, tracking=True,
                              default=compute_crm_user_id)
    is_assigned = fields.Boolean(string=_('Confirm Lead'))
    date_setting_lead = fields.Datetime(string=_('Date Auto Assigned Lead'))

    def lead_assigned(self):
        self.user_id = False
        if self.env.user.id:
            user_id = self.env.user.id
            self.user_id = user_id
            self.is_assigned = True

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            # 1_______________________Create 3 field : campaign_id, source_id ,tag_id __________________________
            print(val)
            if 'campaign_id' in val or 'source_id' in val or 'tag_ids' in val:
                if val['campaign_id'] != False \
                        and val['source_id'] != False \
                        and len(val['tag_ids'][0][2]) > 0:
                    list_tag = val['tag_ids'][0][2]
                    rule_setting = self.env['crm.lead.assignation.line'].search([
                        ('campaign_id', '=', val['campaign_id']),
                        ('source_id', '=', val['source_id']),
                        ('tag_id', '=', list_tag[0]),
                    ])
                    if rule_setting:
                        priority_rule = rule_setting[0]
                        for i in range(1, len(rule_setting)):
                            if priority_rule.sequence > rule_setting[i].sequence:
                                priority_rule = rule_setting[i]
                        # update val
                        val['team_id'] = priority_rule.team_id.id
                        val['date_setting_lead'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if priority_rule.user_ids:
                            val['user_id'] = priority_rule.user_ids[0].id
                # 2_______________________Create 2 field : campaign_id, source_id  __________________________
                elif val['campaign_id'] != False \
                        and val['source_id'] != False \
                        and len(val['tag_ids'][0][2]) == 0:
                    rule_setting = self.env['crm.lead.assignation.line'].search([
                        ('campaign_id', '=', val['campaign_id']),
                        ('source_id', '=', val['source_id']),
                        ('tag_id', '=', False),
                    ])
                    if rule_setting:
                        priority_rule = rule_setting[0]
                        for i in range(1, len(rule_setting)):
                            if priority_rule.sequence > rule_setting[i].sequence:
                                priority_rule = rule_setting[i]
                        # update val
                        val['team_id'] = priority_rule.team_id.id
                        val['date_setting_lead'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if priority_rule.user_ids:
                            val['user_id'] = priority_rule.user_ids[0].id
                # 3 _______________________Create 2 field : campaign_id ,tag_id __________________________
                elif val['campaign_id'] != False \
                        and val['source_id'] == False \
                        and len(val['tag_ids'][0][2]) > 0:
                    list_tag = val['tag_ids'][0][2]
                    rule_setting = self.env['crm.lead.assignation.line'].search([
                        ('campaign_id', '=', val['campaign_id']),
                        ('source_id', '=', False),
                        ('tag_id', '=', list_tag[0]),
                    ])
                    if rule_setting:
                        priority_rule = rule_setting[0]
                        for i in range(1, len(rule_setting)):
                            if priority_rule.sequence > rule_setting[i].sequence:
                                priority_rule = rule_setting[i]
                        # update val
                        val['team_id'] = priority_rule.team_id.id
                        val['date_setting_lead'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if priority_rule.user_ids:
                            val['user_id'] = priority_rule.user_ids[0].id
                # 4 _______________________Create 2 field : source_id ,tag_id ______________________
                elif val['campaign_id'] == False \
                        and val['source_id'] != False \
                        and len(val['tag_ids'][0][2]) > 0:
                    list_tag = val['tag_ids'][0][2]
                    rule_setting = self.env['crm.lead.assignation.line'].search([
                        ('campaign_id', '=', False),
                        ('source_id', '=', val['source_id']),
                        ('tag_id', '=', list_tag[0]),
                    ])
                    if rule_setting:
                        priority_rule = rule_setting[0]
                        for i in range(1, len(rule_setting)):
                            if priority_rule.sequence > rule_setting[i].sequence:
                                priority_rule = rule_setting[i]
                        # update val
                        val['team_id'] = priority_rule.team_id.id
                        val['date_setting_lead'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if priority_rule.user_ids:
                            val['user_id'] = priority_rule.user_ids[0].id
                # 5 _______________________Create one field : campaign_id __________________________
                elif val['campaign_id'] != False \
                        and val['source_id'] == False \
                        and len(val['tag_ids'][0][2]) == 0:
                    rule_setting = self.env['crm.lead.assignation.line'].search([
                        ('campaign_id', '=', val['campaign_id']),
                        ('source_id', '=', False),
                        ('tag_id', '=', False),
                    ])
                    if rule_setting:
                        # Find rule setting by min sequence
                        priority_rule = rule_setting[0]
                        for i in range(1, len(rule_setting)):
                            if priority_rule.sequence > rule_setting[i].sequence:
                                priority_rule = rule_setting[i]
                        # update val
                        val['team_id'] = priority_rule.team_id.id
                        val['date_setting_lead'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if priority_rule.user_ids:
                            val['user_id'] = priority_rule.user_ids[0].id
                # 6 _______________________Create one field : source_id __________________________
                elif val['source_id'] != False \
                        and val['campaign_id'] == False \
                        and len(val['tag_ids'][0][2]) == 0:
                    rule_setting = self.env['crm.lead.assignation.line'].search([
                        ('campaign_id', '=', False),
                        ('source_id', '=', val['source_id']),
                        ('tag_id', '=', False),
                    ])
                    if rule_setting:
                        # Find rule setting by min sequence
                        priority_rule = rule_setting[0]
                        for i in range(1, len(rule_setting)):
                            if priority_rule.sequence > rule_setting[i].sequence:
                                priority_rule = rule_setting[i]
                        # update val
                        val['team_id'] = priority_rule.team_id.id
                        val['date_setting_lead'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if priority_rule.user_ids:
                            val['user_id'] = priority_rule.user_ids[0].idd
                # 7 _______________________Create one field : tag_id __________________________
                elif len(val['tag_ids'][0][2]) > 0 \
                        and val['campaign_id'] == False \
                        and val['source_id'] == False:
                    list_tag = val['tag_ids'][0][2]
                    rule_setting = self.env['crm.lead.assignation.line'].search([
                        ('campaign_id', '=', False),
                        ('source_id', '=', False),
                        ('tag_id', '=', list_tag[0]),
                    ])
                    if rule_setting:
                        # Find rule setting by min sequence
                        priority_rule = rule_setting[0]
                        for i in range(1, len(rule_setting)):
                            if priority_rule.sequence > rule_setting[i].sequence:
                                priority_rule = rule_setting[i]
                        # update val
                        val['team_id'] = priority_rule.team_id.id
                        val['date_setting_lead'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if priority_rule.user_ids:
                            val['user_id'] = priority_rule.user_ids[0].id
                return super(CrmLead, self).create(val)
            else:
                return super(CrmLead, self).create(vals_list)

    def write(self, vals):
        res = super(CrmLead, self).write(vals)
        # _________________________ Change 1 of 3 field : campaign_id, source_id ,tag_id _________________________
        if 'campaign_id' in vals or 'source_id' in vals or 'tag_ids' in vals:
            if self.campaign_id:
                campaign_id = self.campaign_id.id
            else:
                campaign_id = False
            if self.source_id:
                source_id = self.source_id.id
            else:
                source_id = False
            if self.tag_ids:
                tag_ids = self.tag_ids[0].id
            else:
                tag_ids = False

            rule_setting = self.env['crm.lead.assignation.line'].search([
                ('campaign_id', '=', campaign_id),
                ('source_id', '=', source_id),
                ('tag_id', '=', tag_ids),
            ])
            if rule_setting:
                # Find rule setting by min sequence
                priority_rule = rule_setting[0]
                for i in range(1, len(rule_setting)):
                    if priority_rule.sequence > rule_setting[i].sequence:
                        priority_rule = rule_setting[i]
                if priority_rule.user_ids:
                    user_id = priority_rule.user_ids[0].id
                else:
                    user_id = False
                self.update({
                    'user_id': user_id,
                    'team_id': priority_rule.team_id.id,
                    'date_setting_lead': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        return res

    def auto_refresh_assigned(self):
        leads = self.env['crm.lead'].search([('is_assigned', '=', False),
                                             ('date_setting_lead', '!=', False),
                                             ('user_id', '!=', False),
                                             ])
        setting = self.env['crm.lead.assignation.setting'].search([], limit=1)
        if setting:
            time_setup_cron_job = setting.withdraw_after
            if time_setup_cron_job > 0:
                for lead in leads:
                    date_setting_lead = lead.date_setting_lead
                    current_time = int(datetime.now().timestamp())
                    date_setting_lead_time = int(date_setting_lead.timestamp())

                    duration = current_time - date_setting_lead_time
                    time_setup_cron_job_seconds = time_setup_cron_job * 60
                    if duration > time_setup_cron_job_seconds:
                        lead.update({
                            'user_id': False,
                            'team_id': False,
                        })
