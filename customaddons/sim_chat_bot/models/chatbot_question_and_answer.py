from odoo import api, fields, models


class ChatbotQuestionAndAnswer(models.Model):
    _name = "chat.bot.question.and.answer"
    _rec_name = "name"
    #
    name = fields.Text(string="Tên kịch bản",
                       help="Lời chào khách hàng khi họ inbox tới page của công ty.\n Để đặt lời chào: 'Xin chào anh Đào Văn A đã quan tâm tới dịch vụ của chúng tôi', \n Chúng ta đặ theo cú pháp: 'Xin chào XXX đã quan tâm tới dịch vụ của chúng tôi'")
    exception = fields.Text(string="Câu thoại ngoại lệ",
                            help="Sử dụng khi câu trả lời của khách hàng nằm ngoài kịch bản")
    prepare_question_ids = fields.One2many(string="Cấu hình chuẩn bị các câu hỏi",
                                           inverse_name='chat_bot_question_answer_id', comodel_name="prepare.question")
