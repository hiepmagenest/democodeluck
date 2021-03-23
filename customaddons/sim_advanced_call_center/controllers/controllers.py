# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class AdvancedCallCenter(http.Controller):

    def _format_string(self, string):
        if len(string) > 40:
            return string[1:40] + '...'
        else:
            return string

    @http.route('/crm_call/api/callcenter/call_in', type='http', auth='public', methods=['GET'])
    # @http.route('/api/callcenter/incoming_call', type='http', auth='public', methods=['GET'])
    def call_incoming(self, **kw):
        call_id = None
        phone = None
        employee = None
        message = {}
        title = {}
        template = None
        has_customer = False
        customer_name = "Un-Known"
        if 'extension' in kw:
            call_id = kw['extension']
        if call_id:
            employee = request.env['hr.employee'].sudo().search([('call_id', '=', call_id)], limit=1)
            if employee.sudo().user_id:
                if employee.sudo().user_id.lang == 'vi_VN':
                    title.update({
                        'care': 'Nhân viên chăm sóc: ',
                        'last_sale': 'Nhân viên sale: ',
                        'sale': 'Đơn hàng:',
                        'purchase': 'Đơn mua hàng:',
                        'task': 'Xử lý hồ sơ',
                    })
                else:
                    title.update({
                        'care': 'Employee Care: ',
                        'last_sale': 'Last Sale Employee: ',
                        'sale': 'Sale Orders',
                        'purchase': ' Purchase Orders',
                        'task': 'Tasks',
                    })
        if 'phone' in kw:
            phone = kw['phone']
            customer = request.env['res.partner'].sudo().search([('phone', '=', phone)], limit=1)
            customer_name = customer.name if customer else "Un-Known"
            # customer_name = self._format_string(customer_name)
            # Customer information
            if customer:
                has_customer = True
                # find all sale order relate
                values = []
                data = {}
                so_amount = 0
                po_amount = 0
                task_amount = 0
                # orders = request.env['sale.order'].sudo().search([('partner_id', '=', customer.id)])
                # if len(orders) > 0:
                #     so_amount += len(orders)
                #     for so in orders:
                #         relate_task = []
                #         relate_po = []
                #         create_at = so.date_order.strftime("%d/%m/%Y")
                #         tasks = request.env['project.task'].sudo().search([('sale_order_id', '=', so.id)])
                #         for task in tasks:
                #             task_amount += 1
                #             task_date = task.create_date.strftime("%d/%m/%Y")
                #             relate_task.append("Task:" + task.name + "(" + task_date + "-" + task.stage_id.name + ")")
                #         # for po in so.purchase_order_ids:
                #         #     po_amount += 1
                #         #     date = po.create_date.strftime("%d/%m/%Y")
                #         #     relate_po.append("PO:" + po.name + "(" + date + "-" + po.state + ")")
                #         values.append({
                #             'so': "SO:" + so.name + "(" + create_at + "-" + so.state + ")",
                #             'po': relate_po,
                #             'task': relate_task,
                #         })
                # data.update({
                #     'so_amount': so_amount,
                #     'po_amount': po_amount,
                #     'task_amount': task_amount,
                #     'sale_take_care': customer.sale_employee_for_partner_id.name
                # })
                template = request.env.ref('sim_advanced_call_center.call_customer_info')._render({
                    'body': values,
                    'data': data,
                    'title': title
                }, engine='ir.qweb', minimal_qcontext=True)
        if employee:
            message.update({
                'uid': employee.user_id.id,
                'phone': phone,
                'name': customer_name,
                'customer': has_customer,
                'description': template
            })
            request.env['bus.bus'].sendone('show_call_effect_' + str(employee.user_id.id), message)
        return "True"
