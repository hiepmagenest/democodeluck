from odoo import fields, models, api, _
from collections import defaultdict
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging
import pytz
import json

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('overdue', 'Overdue'),
        ('today', 'Today'),
        ('planned', 'Planned'),
        ('done', 'Done')
    ], 'State',
        compute='_compute_state')
    activity_result = fields.Many2one('mail.activity.type.result', 'Result')

    def action_view_source_document(self):
        return {
            'name': _('Lead'),
            'view_mode': 'form',
            'view_id': self.env.ref('crm.crm_lead_view_form').id,
            'res_model': self.res_model,
            # 'context': "{'id':'out_invoice'}",
            # 'domain': [('id', '=', self.res_id)],
            'type': 'ir.actions.act_window',
            'res_id': self.res_id,
        }

    @api.depends('date_deadline')
    def _compute_state(self):
        for record in self.filtered(lambda activity: activity.date_deadline):
            tz = record.user_id.sudo().tz
            date_deadline = record.date_deadline
            record.state = record._compute_state_from_date(date_deadline, tz)

    @api.model
    def _compute_state_from_date(self, date_deadline, tz=False):
        date_deadline = fields.Date.from_string(date_deadline)
        today_default = date.today()
        today = today_default
        if self.active:
            if tz:
                today_utc = pytz.UTC.localize(datetime.utcnow())
                today_tz = today_utc.astimezone(pytz.timezone(tz))
                today = date(year=today_tz.year, month=today_tz.month, day=today_tz.day)
            diff = (date_deadline - today)
            if diff.days == 0:
                return 'today'
            elif diff.days < 0:
                return 'overdue'
            else:
                return 'planned'
        else:
            return 'done'

    def _action_done(self, feedback=False, attachment_ids=None):
        """ Private implementation of marking activity as done: posting a message, deleting activity
            (since done), and eventually create the automatical next activity (depending on config).
            :param feedback: optional feedback from user when marking activity as done
            :param attachment_ids: list of ir.attachment ids to attach to the posted mail.message
            :returns (messages, activities) where
                - messages is a recordset of posted mail.message
                - activities is a recordset of mail.activity of forced automically created activities
        """
        # marking as 'done'
        messages = self.env['mail.message']
        next_activities_values = []

        # Search for all attachments linked to the activities we are about to unlink. This way, we
        # can link them to the message posted and prevent their deletion.
        attachments = self.env['ir.attachment'].search_read([
            ('res_model', '=', self._name),
            ('res_id', 'in', self.ids),
        ], ['id', 'res_id'])

        activity_attachments = defaultdict(list)
        for attachment in attachments:
            activity_id = attachment['res_id']
            activity_attachments[activity_id].append(attachment['id'])

        for activity in self:
            # extract value to generate next activities
            if activity.force_next:
                Activity = self.env['mail.activity'].with_context(
                    activity_previous_deadline=activity.date_deadline)  # context key is required in the onchange to set deadline
                vals = Activity.default_get(Activity.fields_get())

                vals.update({
                    'previous_activity_type_id': activity.activity_type_id.id,
                    'res_id': activity.res_id,
                    'res_model': activity.res_model,
                    'res_model_id': self.env['ir.model']._get(activity.res_model).id,
                })
                virtual_activity = Activity.new(vals)
                virtual_activity._onchange_previous_activity_type_id()
                virtual_activity._onchange_activity_type_id()
                next_activities_values.append(virtual_activity._convert_to_write(virtual_activity._cache))

            # post message on activity, before deleting it
            record = self.env[activity.res_model].browse(activity.res_id)
            record.message_post_with_view(
                'mail.message_activity_done',
                values={
                    'activity': activity,
                    'feedback': feedback,
                    'display_assignee': activity.user_id != self.env.user
                },
                subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
                mail_activity_type_id=activity.activity_type_id.id,
                attachment_ids=[(4, attachment_id) for attachment_id in attachment_ids] if attachment_ids else [],
            )

            # Moving the attachments in the message
            # TODO: Fix void res_id on attachment when you create an activity with an image
            # directly, see route /web_editor/attachment/add
            activity_message = record.message_ids[0]
            message_attachments = self.env['ir.attachment'].browse(activity_attachments[activity.id])
            if message_attachments:
                message_attachments.write({
                    'res_id': activity_message.id,
                    'res_model': activity_message._name,
                })
                activity_message.attachment_ids = message_attachments
            messages |= activity_message

        next_activities = self.env['mail.activity'].create(next_activities_values)
        self.sudo().active = False  # will unlink activity, dont access `self` after that
        return messages, next_activities

    def activity_format(self):
        result = super(MailActivity, self).activity_format()
        # activity_type_approval_id = self.env.ref('approvals.mail_activity_data_approval').id
        x=0
        for activity in result:
            if activity['res_model'] == 'crm.lead':
                list = []
                records = self[x].activity_type_id.activity_type_result_ids
                for record in records:
                    val = {
                        'id': record.id,
                        'name': record.name
                    }
                    list.append(val)
                activity['result_vals'] = json.dumps(list)
                x += 1
                # activity['result_vals'] = list
        return result


    @api.model
    def get_result_vals(self):
        list = []
        records = self.active_type_id.activity_type_result_ids
        for record in records:
            val = {
                'id': record.id,
                'name': record.name
            }
            list.append(val)
        return list

    def mark_as_done_2(self, result_id):
        result = self.sudo().env['mail.activity.type.result'].browse(result_id)
        next_activity_type_id = result.next_activity_type_id
        feedback = result.name
        record = self.env[self.res_model].browse(self.res_id)
        record.message_post_with_view(
            'mail.message_activity_done',
            values={
                'activity': self,
                'feedback': feedback,
                'display_assignee': self.user_id != self.env.user
            },
            subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
            mail_activity_type_id=self.activity_type_id.id,
        )
        if result.next_activity_type_id:
            today = date.today()
            next_activity_deadline = result.next_activity_deadline
            date_deadline = today + timedelta(days=next_activity_deadline)
            vals = [
                {
                    'res_model': self.res_model,
                    'res_model_id': self.res_model_id.id,
                    'activity_type_id': next_activity_type_id.id,
                    'user_id': self.user_id.id,
                    'previous_activity_type_id': self.activity_type_id.id,
                    'active': True,
                    'res_id': self.res_id,
                    'date_deadline': date_deadline,
                }
            ]
            self.env['mail.activity'].create(vals)
        if result.crm_stage_id:
            record.stage_id = result.crm_stage_id.id
        self.sudo().active = False
        print(self)
        print(result.name)




