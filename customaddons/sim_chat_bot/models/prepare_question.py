from odoo import api, fields, models


class PrepareQuestion(models.Model):
    _name = "prepare.question"
    # _rec_name = "question"
    _order = 'sequence'

    sequence = fields.Integer(string="Thứ tự")
    response_answer = fields.Text(string="Câu trả lời khách hàng")
    apply_for_question_id = fields.Many2one(string="Áp dụng cho câu hỏi", comodel_name="tree.question")
    next_question_id = fields.Many2one(string="Câu hỏi tiếp theo", comodel_name="tree.question")
    is_question_get_phone = fields.Boolean(string="Câu hỏi lấy số điện thoại",
                                           related='next_question_id.is_question_get_phone')
    is_question_get_email = fields.Boolean(string="Câu hỏi lấy email khách hàng",
                                           related='next_question_id.is_question_get_email')
    chat_bot_question_answer_id = fields.Many2one(string="Kịch bản Chatbot",
                                                  comodel_name="chat.bot.question.and.answer")
