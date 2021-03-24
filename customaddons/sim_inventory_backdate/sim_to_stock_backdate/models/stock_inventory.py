from odoo import models
from odoo.tools import float_compare


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    def action_validate(self):
        # somewhere this is called with multi in self, so we need to fallback to the default behaviour in such the case
        if not self._context.get('manual_validate_date_time') and self.env.user.has_group(
                'sim_to_backdate.group_backdate') and not len(self) > 1:
            view = self.env.ref('sim_to_stock_backdate.stock_inventory_backdate_wizard_form_view')
            ctx = dict(self._context or {})
            ctx.update({'default_inventory_id': self.id})
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'stock.inventory.backdate.wizard',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'context': ctx,
            }
        elif self.env.user.has_group('sim_to_backdate.group_backdate') and not len(self) > 1:
            inventory_lines = self.line_ids.filtered(lambda l: l.product_id.tracking in ['lot',
                                                                                         'serial'] and not l.prod_lot_id and l.theoretical_qty != l.product_qty)
            lines = self.line_ids.filtered(lambda l: float_compare(l.product_qty, 1,
                                                                   precision_rounding=l.product_uom_id.rounding) > 0 and l.product_id.tracking == 'serial' and l.prod_lot_id)
            # this should call stock track confirmation wizard for tracked products.
            # in such situation, we inject backdate into context
            if inventory_lines and not lines:
                res = super(StockInventory, self).action_validate()
                if isinstance(res, dict):
                    res.update({'context': {
                        'manual_validate_date_time': self._context.get('manual_validate_date_time', False)}})
                return res
        return super(StockInventory, self).action_validate()
