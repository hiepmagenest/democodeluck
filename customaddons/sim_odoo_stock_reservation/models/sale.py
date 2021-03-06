# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_stock_reservation_order = fields.Boolean(
        string="Apply Stock Reservation?",
        copy=False,
    )
    stock_move_ids = fields.One2many(
        'stock.move.reservation',
        'custome_sale_order_id',
        string="Stock Reservations",
        copy=False,
    )
    is_stock_reserv_created = fields.Boolean(
        string="Is Stock Created",
        copy=False,
    )

    # @api.multi
    def action_confirm(self):
        for order in self:
            order_line = order.order_line
            stock_move_reservation_ids = self.env['stock.move.reservation'].search([
                ('custome_so_line_id', 'in', order_line.ids),
                ('state', '!=', 'cancel')
            ])
            if stock_move_reservation_ids:
                raise ValidationError("Please Cancel Reserved Stock")
        return super(SaleOrder, self).action_confirm()

    # @api.multi
    def action_create_stock_reservation(self):
        self.ensure_one()
        return {
            'name': _('Stock Reservation'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.reservation',
            'view_id': self.env.ref('sim_odoo_stock_reservation.wiz_stock_reservation_view').id,
            'type': 'ir.actions.act_window',
            'context': {
                'default_sale_order_id': self.id,
                'current_sale_order_id': self.id,
            },
            'target': 'new'
        }

    # @api.multi
    def action_cancel_stock_reservation(self):
        self.ensure_one()
        order_line_ids = self.order_line
        stock_move_reservation_ids = self.env['stock.move.reservation'].search([
            ('custome_so_line_id', 'in', order_line_ids.ids),
            ('state', '!=', 'cancel')
        ])
        stock_move_ids = self.env['stock.move']
        for move_res in stock_move_reservation_ids:
            stock_move_ids += move_res.move_id
        if stock_move_ids:
            result = stock_move_ids._action_cancel()
            if result:
                order_line_ids.write({
                    'stock_reserved_qty': 0.0,
                })
                self.is_stock_reserv_created = False
        else:
            if not self._context.get('is_unlink_reserved_stock'):
                raise ValidationError("No any stock reservation records found.")

    # @api.multi
    def action_cancel(self):
        self.ensure_one()
        order_line_ids = self.order_line
        stock_move_reservation_ids = self.env['stock.move.reservation'].search([
            ('custome_so_line_id', 'in', order_line_ids.ids),
        ])
        if stock_move_reservation_ids:
            ctx = self._context.copy()
            ctx.update({'is_unlink_reserved_stock': True})
            self.with_context(ctx).action_cancel_stock_reservation()
            #            self.action_cancel_stock_reservation()
            stock_move_reservation_ids.unlink()
        return super(SaleOrder, self).action_cancel()

    # @api.multi
    def action_view_reserved_stock(self):
        self.ensure_one()
        action = self.env.ref("sim_odoo_stock_reservation.action_stock_move_reserv_product").read()[0]
        action['domain'] = [('id', 'in', self.stock_move_ids.ids)]
        return action


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    stock_reserved_qty = fields.Float(
        string="Stock Reserved Quantity"
    )

    # @api.multi
    def write(self, vals):
        if 'product_id' in vals:
            for rec in self:
                stock_move_reservation_ids = self.env['stock.move.reservation'].search([
                    ('custome_so_line_id', '=', rec.id),
                    ('state', '!=', 'cancel')
                ])
                stock_move_ids = self.env['stock.move']
                for move_res in stock_move_reservation_ids:
                    stock_move_ids += move_res.move_id
                if stock_move_ids:
                    result = stock_move_ids._action_cancel()
                    if result:
                        vals.update(stock_reserved_qty=0.0)
        #                        vals.update(is_stock_reserv_created=True)
        return super(SaleOrderLine, self).write(vals)

    # @api.multi
    def unlink(self):
        for rec in self:
            stock = self.env['stock.move.reservation'].search([('custome_so_line_id', '=', rec.id)])
            stock_res_move_ids = stock.mapped('move_id')
            stock_res_move_ids._action_cancel()
            stock.unlink()
        return super(SaleOrderLine, self).unlink()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
