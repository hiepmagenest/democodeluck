from odoo import fields, models


class StockScrapBackdateWizard(models.TransientModel):
    _name = 'stock.scrap.backdate.wizard'
    _inherit = 'abstract.inventory.backdate.wizard'
    _description = 'Stock Scrap Backdate Wizard'

    date = fields.Datetime(string='Actual Scrap Date')
    scrap_id = fields.Many2one('stock.scrap', string="Stock Scrap", required=True, ondelete='cascade')

    def process(self):
        self.ensure_one()
        self.scrap_id.write({'date_done': self.date})
        date = fields.Date.context_today(self, self.date)
        return self.scrap_id.with_context(
            manual_validate_date_time=date,
            force_period_date=self.date
        ).action_validate()
