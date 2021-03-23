from odoo import api, fields, models


class TreeQuestion(models.Model):
    _name = "tree.question"
    _rec_name = "summary_of_question"

    question = fields.Text(string="Câu thoại")
    summary_of_question = fields.Text(string="Tóm tắt câu hỏi")
    selection_answer_ids = fields.One2many(string="Các lựa chọn trả lời", comodel_name="tree.answer",
                                           inverse_name="tree_question_id")
    is_question_get_phone = fields.Boolean(string="Câu hỏi lấy số điện thoại")
    is_question_get_email = fields.Boolean(string="Câu hỏi lấy email khách hàng")
    link_image_url = fields.Char(string="Link ảnh (nếu có)")
