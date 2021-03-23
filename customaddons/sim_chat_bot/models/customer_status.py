from odoo import api, fields, models


class CustomerStatus(models.Model):
    _name = "chat.bot.customer.status"
    _rec_name = "name_customer"

    name_customer = fields.Char(string="Tên khách hàng")
    sender_id = fields.Char(string="Mã khách hàng", help="Mã sender_id từ facebook")
    has_visited = fields.Boolean(string="Đã từng ghé thăm page", default=False)
    last_question_id = fields.Many2one(string="Câu hỏi cuối cùng", comodel_name="tree.question")
