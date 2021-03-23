from odoo import api, fields, models


class TreeAnswer(models.Model):
    _name = "tree.answer"
    _rec_name = "answer"

    tree_question_id = fields.Many2one(comodel_name="tree.question", string="Dành cho câu hỏi")
    answer = fields.Text(string="Câu trả lời")
