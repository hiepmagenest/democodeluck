# -*- coding: utf-8 -*-
import pytz
from pymessenger import Bot
import requests
from odoo import http
from odoo.http import request
from datetime import datetime

FB_API_URL = 'https://graph.facebook.com/'
VERIFY_TOKEN = 'flexfit'  # <paste your verify token here>


# paste your page access token here>"


class AdvancedChatbot(http.Controller):

    @http.route("/verify", auth="public", methods=['GET'])
    def verify_webhook(self):
        if request.params.get("hub.mode") == "subscribe" and request.params.get("hub.challenge"):
            if not request.params.get("hub.verify_token") == VERIFY_TOKEN:
                return "Verification token mismatch"
            return request.params["hub.challenge"]
        return "Hello world"

    def get_name_user(self, PSID):
        request_endpoint = FB_API_URL + PSID + '?fields=first_name,last_name,profile_pic'
        PAGE_ACCESS_TOKEN = request.env['ir.config_parameter'].sudo().get_param('PAGE_ACCESS_TOKEN')
        response = requests.get(
            request_endpoint,
            params={'access_token': PAGE_ACCESS_TOKEN}
        )
        name = "bạn"
        # print(response.json())
        if 'first_name' in response.json():
            name = name.replace("bạn", response.json()['first_name'])
            if 'last_name' in response.json():
                name += " " + response.json()['last_name']
        return name

    def get_orther_infor(self, PSID):
        request_endpoint = FB_API_URL + PSID + '?fields=id,name,email,birthday,address,hometown,gender,location'
        PAGE_ACCESS_TOKEN = request.env['ir.config_parameter'].sudo().get_param('PAGE_ACCESS_TOKEN')
        response = requests.get(
            request_endpoint,
            params={'access_token': PAGE_ACCESS_TOKEN}
        )
        # print(response.json())
        # name = "bạn"
        # # print(response.json())
        # if 'first_name' in response.json():
        #     name = name.replace("bạn", response.json()['first_name'])
        #     if 'last_name' in response.json():
        #         name += " " + response.json()['last_name']
        return response

    # @http.route('/verify', type="json", auth="public", methods=['POST'])
    # def webhook2(self):
    #     PAGE_ACCESS_TOKEN = request.env['ir.config_parameter'].sudo().get_param('PAGE_ACCESS_TOKEN')
    #     bot = Bot(PAGE_ACCESS_TOKEN, api_version="6.0")
    #     data = request.jsonrequest
    #     print(data)
    #     if 'object' in data:
    #         if data['object'] == "page":
    #             entries = data['entry']
    #             for entry in entries:
    #                 if 'messaging' in entry:
    #                     messaging = entry['messaging']
    #                     for messaging_event in messaging:
    #                         sender_id = messaging_event['sender']['id']
    #                         if 'message' in messaging_event and sender_id != '100213761580617':
    #                             payload = {
    #                                 "recipient": {
    #                                     "id": sender_id
    #                                 },
    #                                 "message": {
    #                                     "attachment": {
    #                                         "type": "template",
    #                                         "payload": {
    #                                             "template_type": "generic",
    #                                             "elements": [
    #                                                 {
    #                                                     "title": "Welcome to Flexfit!",
    #                                                     "image_url": "https://flexfit.vn/wp-content/uploads/2018/08/92250224_915597475538404_5995180832275300352_o.jpg",
    #                                                     "subtitle": "	Xin chào quý khách ghé thăm Flexfit. Chúng tôi có thể giúp gì cho quý khách?",
    #                                                     "default_action": {
    #                                                         "type": "web_url",
    #                                                         "url": "https://flexfit.vn/",
    #                                                         "webview_height_ratio": "tall",
    #                                                     },
    #                                                     "buttons": [
    #                                                         {
    #                                                             "type": "postback",
    #                                                             "title": "Thiết kế và thi công",
    #                                                             "payload": "<POSTBACK_PAYLOAD>"
    #                                                         }, {
    #                                                             "type": "postback",
    #                                                             "title": "Sản phẩm và phụ kiện",
    #                                                             "payload": "<POSTBACK_PAYLOAD>"
    #                                                         }
    #                                                         , {
    #                                                             "type": "postback",
    #                                                             "title": "Thông tin khuyến mãi",
    #                                                             "payload": "<POSTBACK_PAYLOAD>"
    #                                                         }
    #                                                     ]
    #                                                 },
    #                                             ]
    #                                         }
    #                                     }
    #                                 }}
    #
    #                             bot.send_raw(payload)
    #                             # bot.send_image_url(recipient_id=sender_id, image_url='https://flexfit.vn/wp-content/uploads/2018/08/92250224_915597475538404_5995180832275300352_o.jpg')
    #                         else:
    #                             return "ok"

    @http.route('/verify', type="json", auth="public", methods=['POST'])
    def webhook(self):
        # lay page access (cai dat trong params_meter
        PAGE_ACCESS_TOKEN = request.env['ir.config_parameter'].sudo().get_param('PAGE_ACCESS_TOKEN')
        # MY_FACEBOOK_PAGE_ID dùng để detect xem message của page hay của user
        MY_FACEBOOK_PAGE_ID = request.env['ir.config_parameter'].sudo().get_param('MY_FACEBOOK_PAGE_ID')
        if not MY_FACEBOOK_PAGE_ID:
            MY_FACEBOOK_PAGE_ID = 1
        bot = Bot(PAGE_ACCESS_TOKEN, api_version="6.0")
        if PAGE_ACCESS_TOKEN:
            # lay request cua facebook
            data = request.jsonrequest
            if data['object'] == "page":
                entries = data['entry']
                for entry in entries:
                    if 'messaging' in entry:
                        messaging = entry['messaging']
                        for messaging_event in messaging:
                            # chi lay message phan hoi cua khach hang
                            if 'message' in messaging_event or 'postback' in messaging_event:
                                try:
                                    sender_id = messaging_event['sender']['id']
                                    name_user = self.get_name_user(sender_id)
                                    lead = None
                                    if sender_id != MY_FACEBOOK_PAGE_ID:
                                        # tim lead da chat facebook truoc do
                                        lead = request.env['crm.lead'].sudo().search(
                                            [('facebook_sender_id', '=', sender_id)], limit=1)
                                        # khong co tao moi
                                        if not lead:
                                            lead = request.env['crm.lead'].sudo().create({
                                                'name': name_user,
                                                'type': 'lead',
                                                'facebook_sender_id': sender_id
                                            })
                                    local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                                    # mot message co the la 1.message khach hang hoi minh, 2.message minh da tra loi khach hang
                                    # kiem tra message nay la cua minh gui khach hang hay khong
                                    if sender_id == MY_FACEBOOK_PAGE_ID:
                                        return
                                    # Tìm thằng user đã ghé thăm page
                                    sender = request.env['chat.bot.customer.status'].sudo().search(
                                        [('sender_id', '=', sender_id)], limit=1)
                                    # nếu không có tạo mới lịch sử ghé thăm page
                                    if not sender:
                                        sender = request.env['chat.bot.customer.status'].sudo().create({
                                            'sender_id': sender_id,
                                            'name_customer': name_user
                                        })
                                    has_visited = True
                                    if sender:
                                        if not sender.has_visited:
                                            has_visited = sender.has_visited
                                            sender.sudo().has_visited = True
                                    # nếu là ghé thăm page lần đầu
                                    if not has_visited:
                                        query = ''
                                        if 'message' in messaging_event:
                                            query = messaging_event['message']['text']
                                        elif 'postback' in messaging_event:
                                            query = messaging_event['postback']['title']
                                        if len(query) > 0:
                                            lead.sudo().description = "\n" + str(
                                                datetime.now().astimezone(local_tz).strftime(
                                                    '%d/%m/%Y %H:%M:%S')) + " Khách hàng: \n\t" + query
                                        # chuẩn bị câu hỏi cho user (trường hợp lần đầu tiên ghé thăm
                                        init_bot = request.env['prepare.question'].sudo().search(
                                            [('apply_for_question_id', '=', False), ('response_answer', '=', False)],
                                            limit=1)
                                        if init_bot:
                                            # chuẩn bị câu hỏi tiếp theo
                                            if init_bot.next_question_id:
                                                sender.last_question_id = init_bot.next_question_id
                                                quick_replies = []
                                                # TH1: next question có cả ảnh vs các button quick reply
                                                if init_bot.next_question_id.selection_answer_ids and init_bot.next_question_id.link_image_url:
                                                    # Trả lời text trước
                                                    bot.send_text_message(sender_id, str(
                                                        init_bot.next_question_id.question).replace("user_name",
                                                                                                    name_user))
                                                    # log vào lead
                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                        datetime.now().astimezone(local_tz).strftime(
                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                        init_bot.next_question_id.question.replace("user_name",
                                                                                                   name_user)) if lead.sudo().description else "\n" + str(
                                                        datetime.now().astimezone(local_tz).strftime(
                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                        init_bot.next_question_id.question.replace("user_name",
                                                                                                   name_user))
                                                    # trả lời = template
                                                    for selection in init_bot.next_question_id.selection_answer_ids:
                                                        if selection.answer:
                                                            quick_replies.append({
                                                                "type": "postback",
                                                                "title": str(selection.answer).replace("user_name",
                                                                                                       name_user),
                                                                "payload": "<POSTBACK_PAYLOAD>"
                                                            })
                                                    payload = {
                                                        "recipient": {
                                                            "id": sender_id
                                                        },
                                                        "message": {
                                                            "attachment": {
                                                                "type": "template",
                                                                "payload": {
                                                                    "template_type": "generic",
                                                                    "elements": [
                                                                        {
                                                                            "title": "Welcome to Flexfit!",
                                                                            "image_url": str(
                                                                                init_bot.next_question_id.link_image_url),
                                                                            "subtitle": "	Xin chào quý khách ghé thăm Flexfit. Chúng tôi có thể giúp gì cho quý khách?",
                                                                            "default_action": {
                                                                                "type": "web_url",
                                                                                "url": "https://flexfit.vn/",
                                                                                "webview_height_ratio": "tall",
                                                                            },
                                                                            "buttons": quick_replies,
                                                                        },
                                                                    ]
                                                                }
                                                            }
                                                        }}
                                                    bot.send_raw(payload)
                                                # TH2: next question có các button quick reply nhưng ko có ảnh
                                                elif init_bot.next_question_id.selection_answer_ids and not init_bot.next_question_id.link_image_url:
                                                    # Trả lời text trước
                                                    bot.send_text_message(sender_id, str(
                                                        init_bot.next_question_id.question).replace("user_name",
                                                                                                    name_user))
                                                    # log vào lead
                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                        datetime.now().astimezone(local_tz).strftime(
                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                        init_bot.next_question_id.question.replace("user_name",
                                                                                                   name_user)) if lead.sudo().description else "\n" + str(
                                                        datetime.now().astimezone(local_tz).strftime(
                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                        init_bot.next_question_id.question.replace("user_name",
                                                                                                   name_user))
                                                    # trả lời = template
                                                    for selection in init_bot.next_question_id.selection_answer_ids:
                                                        if selection.answer:
                                                            quick_replies.append({
                                                                "type": "postback",
                                                                "title": str(selection.answer).replace("user_name",
                                                                                                       name_user),
                                                                "payload": "<POSTBACK_PAYLOAD>"
                                                            })
                                                    payload = {
                                                        "recipient": {
                                                            "id": sender_id
                                                        },
                                                        "message": {
                                                            "attachment": {
                                                                "type": "template",
                                                                "payload": {
                                                                    "template_type": "generic",
                                                                    "elements": [
                                                                        {
                                                                            "title": "Welcome to Flexfit!",
                                                                            # "image_url": str(init_bot.next_question_id.link_image_url),
                                                                            "subtitle": "	Xin chào quý khách ghé thăm Flexfit. Chúng tôi có thể giúp gì cho quý khách?",
                                                                            "default_action": {
                                                                                "type": "web_url",
                                                                                "url": "https://flexfit.vn/",
                                                                                "webview_height_ratio": "tall",
                                                                            },
                                                                            "buttons": quick_replies,
                                                                        },
                                                                    ]
                                                                }
                                                            }
                                                        }}
                                                    bot.send_raw(payload)
                                                # TH3: Không có button quick_replies nhưng lại có ảnh:
                                                elif not init_bot.next_question_id.selection_answer_ids and init_bot.next_question_id.link_image_url:
                                                    # Gửi ảnh trước
                                                    bot.send_image_url(recipient_id=sender_id, image_url=str(
                                                        init_bot.next_question_id.link_image_url))
                                                    # Sau đó trả lời text
                                                    bot.send_text_message(sender_id, str(
                                                        init_bot.next_question_id.question).replace("user_name",
                                                                                                    name_user))
                                                    # log vào lead
                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                        datetime.now().astimezone(local_tz).strftime(
                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                        init_bot.next_question_id.question.replace("user_name",
                                                                                                   name_user)) if lead.sudo().description else "\n" + str(
                                                        datetime.now().astimezone(local_tz).strftime(
                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                        init_bot.next_question_id.question.replace("user_name",
                                                                                                   name_user))
                                                # TH4:       Không có cả ảnh vs các button trả lời nhanh
                                                elif not init_bot.next_question_id.selection_answer_ids and not init_bot.next_question_id.link_image_url:
                                                    # Chỉ trả lời mỗi text
                                                    bot.send_text_message(sender_id, str(
                                                        init_bot.next_question_id.question).replace("user_name",
                                                                                                    name_user))
                                                    # log vào lead
                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                        datetime.now().astimezone(local_tz).strftime(
                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                        init_bot.next_question_id.question.replace("user_name",
                                                                                                   name_user)) if lead.sudo().description else "\n" + str(
                                                        datetime.now().astimezone(local_tz).strftime(
                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                        init_bot.next_question_id.question.replace("user_name",
                                                                                                   name_user))

                                                else:
                                                    return

                                    else:
                                        query = ''
                                        if 'message' in messaging_event:
                                            query = messaging_event['message']['text']
                                        elif 'postback' in messaging_event:
                                            query = messaging_event['postback']['title']
                                        if len(query) > 0:
                                            sender = request.env['chat.bot.customer.status'].sudo().search(
                                                [('sender_id', '=', sender_id)], limit=1)
                                            lead.sudo().description = lead.sudo().description + "\n" + str(
                                                datetime.now().astimezone(local_tz).strftime(
                                                    '%d/%m/%Y %H:%M:%S')) + " Khách hàng: \n\t" + query if lead.sudo().description else "\n" + str(
                                                datetime.now().astimezone(local_tz).strftime(
                                                    '%d/%m/%Y %H:%M:%S')) + " Khách hàng: \n\t" + query
                                            if sender:
                                                # nếu là câu hỏi xin sdt thì ghi vào trường sdt của lead
                                                if sender.last_question_id.is_question_get_phone:
                                                    lead.phone = str(query)
                                                # nếu là câu hỏi xin mail thì ghi vào trường mail của lead
                                                if sender.last_question_id.is_question_get_email:
                                                    lead.email_from = str(query)
                                                if sender.last_question_id:
                                                    # chuẩn bị câu trả lời map vs cả question cũ và answer
                                                    init_bot = request.env['prepare.question'].sudo().search(
                                                        [('apply_for_question_id', '=', sender.last_question_id.id),
                                                         ('response_answer', '=', query)],
                                                        limit=1)
                                                    # nếu có tìm đc câu hỏi map vs cả 2
                                                    if init_bot:
                                                        if init_bot.next_question_id:
                                                            sender.last_question_id = init_bot.next_question_id
                                                            quick_replies = []
                                                            if init_bot.next_question_id.selection_answer_ids and init_bot.next_question_id.link_image_url:
                                                                # Trả lời text trước
                                                                bot.send_text_message(sender_id, str(
                                                                    init_bot.next_question_id.question).replace(
                                                                    "user_name", name_user))
                                                                # log vào lead
                                                                lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                    datetime.now().astimezone(local_tz).strftime(
                                                                        '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                    init_bot.next_question_id.question.replace(
                                                                        "user_name",
                                                                        name_user)) if lead.sudo().description else "\n" + str(
                                                                    datetime.now().astimezone(local_tz).strftime(
                                                                        '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                    init_bot.next_question_id.question.replace(
                                                                        "user_name", name_user))
                                                                # trả lời = template
                                                                for selection in init_bot.next_question_id.selection_answer_ids:
                                                                    if selection.answer:
                                                                        quick_replies.append({
                                                                            "type": "postback",
                                                                            "title": str(selection.answer).replace(
                                                                                "user_name", name_user),
                                                                            "payload": "<POSTBACK_PAYLOAD>"
                                                                        })
                                                                payload = {
                                                                    "recipient": {
                                                                        "id": sender_id
                                                                    },
                                                                    "message": {
                                                                        "attachment": {
                                                                            "type": "template",
                                                                            "payload": {
                                                                                "template_type": "generic",
                                                                                "elements": [
                                                                                    {
                                                                                        "title": "Welcome to Flexfit!",
                                                                                        "image_url": str(
                                                                                            init_bot.next_question_id.link_image_url),
                                                                                        "subtitle": "	Xin chào quý khách ghé thăm Flexfit. Chúng tôi có thể giúp gì cho quý khách?",
                                                                                        "default_action": {
                                                                                            "type": "web_url",
                                                                                            "url": "https://flexfit.vn/",
                                                                                            "webview_height_ratio": "tall",
                                                                                        },
                                                                                        "buttons": quick_replies,
                                                                                    },
                                                                                ]
                                                                            }
                                                                        }
                                                                    }}
                                                                bot.send_raw(payload)
                                                            # TH2: next question có các button quick reply nhưng ko có ảnh
                                                            elif init_bot.next_question_id.selection_answer_ids and not init_bot.next_question_id.link_image_url:
                                                                # Trả lời text trước
                                                                bot.send_text_message(sender_id, str(
                                                                    init_bot.next_question_id.question).replace(
                                                                    "user_name", name_user))
                                                                # log vào lead
                                                                lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                    datetime.now().astimezone(local_tz).strftime(
                                                                        '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                    init_bot.next_question_id.question.replace(
                                                                        "user_name",
                                                                        name_user)) if lead.sudo().description else "\n" + str(
                                                                    datetime.now().astimezone(local_tz).strftime(
                                                                        '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                    init_bot.next_question_id.question.replace(
                                                                        "user_name", name_user))
                                                                # trả lời = template
                                                                for selection in init_bot.next_question_id.selection_answer_ids:
                                                                    if selection.answer:
                                                                        quick_replies.append({
                                                                            "type": "postback",
                                                                            "title": str(selection.answer).replace(
                                                                                "user_name", name_user),
                                                                            "payload": "<POSTBACK_PAYLOAD>"
                                                                        })
                                                                payload = {
                                                                    "recipient": {
                                                                        "id": sender_id
                                                                    },
                                                                    "message": {
                                                                        "attachment": {
                                                                            "type": "template",
                                                                            "payload": {
                                                                                "template_type": "generic",
                                                                                "elements": [
                                                                                    {
                                                                                        "title": "Welcome to Flexfit!",
                                                                                        # "image_url": str(init_bot.next_question_id.link_image_url),
                                                                                        "subtitle": "	Xin chào quý khách ghé thăm Flexfit. Chúng tôi có thể giúp gì cho quý khách?",
                                                                                        "default_action": {
                                                                                            "type": "web_url",
                                                                                            "url": "https://flexfit.vn/",
                                                                                            "webview_height_ratio": "tall",
                                                                                        },
                                                                                        "buttons": quick_replies,
                                                                                    },
                                                                                ]
                                                                            }
                                                                        }
                                                                    }}
                                                                bot.send_raw(payload)
                                                            # TH3: Không có button quick_replies nhưng lại có ảnh:
                                                            elif not init_bot.next_question_id.selection_answer_ids and init_bot.next_question_id.link_image_url:
                                                                # Gửi ảnh trước
                                                                bot.send_image_url(recipient_id=sender_id,
                                                                                   image_url=str(
                                                                                       init_bot.next_question_id.link_image_url))
                                                                # Sau đó trả lời text
                                                                bot.send_text_message(sender_id, str(
                                                                    init_bot.next_question_id.question).replace(
                                                                    "user_name", name_user))
                                                                # log vào lead
                                                                lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                    datetime.now().astimezone(local_tz).strftime(
                                                                        '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                    init_bot.next_question_id.question.replace(
                                                                        "user_name",
                                                                        name_user)) if lead.sudo().description else "\n" + str(
                                                                    datetime.now().astimezone(local_tz).strftime(
                                                                        '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                    init_bot.next_question_id.question.replace(
                                                                        "user_name", name_user))
                                                            # TH4:       Không có cả ảnh vs các button trả lời nhanh
                                                            elif not init_bot.next_question_id.selection_answer_ids and not init_bot.next_question_id.link_image_url:
                                                                # Chỉ trả lời mỗi text
                                                                bot.send_text_message(sender_id, str(
                                                                    init_bot.next_question_id.question).replace(
                                                                    "user_name", name_user))
                                                                # log vào lead
                                                                lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                    datetime.now().astimezone(local_tz).strftime(
                                                                        '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                    init_bot.next_question_id.question.replace(
                                                                        "user_name",
                                                                        name_user)) if lead.sudo().description else "\n" + str(
                                                                    datetime.now().astimezone(local_tz).strftime(
                                                                        '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                    init_bot.next_question_id.question.replace(
                                                                        "user_name", name_user))

                                                            else:
                                                                return

                                                    else:
                                                        # Nếu ko tìm đc câu hỏi ở trên thì chỉ tìm theo diều kiện về câu hỏi
                                                        init_bot = request.env['prepare.question'].sudo().search([(
                                                            'apply_for_question_id',
                                                            '=',
                                                            sender.last_question_id.id)],
                                                            limit=1)
                                                        if init_bot:
                                                            if init_bot.next_question_id:
                                                                sender.last_question_id = init_bot.next_question_id
                                                                if init_bot.next_question_id.selection_answer_ids and init_bot.next_question_id.link_image_url:
                                                                    # Trả lời text trước
                                                                    bot.send_text_message(sender_id, str(
                                                                        init_bot.next_question_id.question).replace(
                                                                        "user_name", name_user))
                                                                    # log vào lead
                                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        init_bot.next_question_id.question.replace(
                                                                            "user_name",
                                                                            name_user)) if lead.sudo().description else "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        init_bot.next_question_id.question.replace(
                                                                            "user_name", name_user))
                                                                    # trả lời = template
                                                                    for selection in init_bot.next_question_id.selection_answer_ids:
                                                                        if selection.answer:
                                                                            quick_replies.append({
                                                                                "type": "postback",
                                                                                "title": str(selection.answer).replace(
                                                                                    "user_name", name_user),
                                                                                "payload": "<POSTBACK_PAYLOAD>"
                                                                            })
                                                                    payload = {
                                                                        "recipient": {
                                                                            "id": sender_id
                                                                        },
                                                                        "message": {
                                                                            "attachment": {
                                                                                "type": "template",
                                                                                "payload": {
                                                                                    "template_type": "generic",
                                                                                    "elements": [
                                                                                        {
                                                                                            "title": "Welcome to Flexfit!",
                                                                                            "image_url": str(
                                                                                                init_bot.next_question_id.link_image_url),
                                                                                            "subtitle": "	Xin chào quý khách ghé thăm Flexfit. Chúng tôi có thể giúp gì cho quý khách?",
                                                                                            "default_action": {
                                                                                                "type": "web_url",
                                                                                                "url": "https://flexfit.vn/",
                                                                                                "webview_height_ratio": "tall",
                                                                                            },
                                                                                            "buttons": quick_replies,
                                                                                        },
                                                                                    ]
                                                                                }
                                                                            }
                                                                        }}
                                                                    bot.send_raw(payload)
                                                                # TH2: next question có các button quick reply nhưng ko có ảnh
                                                                elif init_bot.next_question_id.selection_answer_ids and not init_bot.next_question_id.link_image_url:
                                                                    # Trả lời text trước
                                                                    bot.send_text_message(sender_id, str(
                                                                        init_bot.next_question_id.question).replace(
                                                                        "user_name", name_user))
                                                                    # log vào lead
                                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        init_bot.next_question_id.question.replace(
                                                                            "user_name",
                                                                            name_user)) if lead.sudo().description else "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        init_bot.next_question_id.question.replace(
                                                                            "user_name", name_user))
                                                                    # trả lời = template
                                                                    for selection in init_bot.next_question_id.selection_answer_ids:
                                                                        if selection.answer:
                                                                            quick_replies.append({
                                                                                "type": "postback",
                                                                                "title": str(selection.answer).replace(
                                                                                    "user_name", name_user),
                                                                                "payload": "<POSTBACK_PAYLOAD>"
                                                                            })
                                                                    payload = {
                                                                        "recipient": {
                                                                            "id": sender_id
                                                                        },
                                                                        "message": {
                                                                            "attachment": {
                                                                                "type": "template",
                                                                                "payload": {
                                                                                    "template_type": "generic",
                                                                                    "elements": [
                                                                                        {
                                                                                            "title": "Welcome to Flexfit!",
                                                                                            # "image_url": str(init_bot.next_question_id.link_image_url),
                                                                                            "subtitle": "	Xin chào quý khách ghé thăm Flexfit. Chúng tôi có thể giúp gì cho quý khách?",
                                                                                            "default_action": {
                                                                                                "type": "web_url",
                                                                                                "url": "https://flexfit.vn/",
                                                                                                "webview_height_ratio": "tall",
                                                                                            },
                                                                                            "buttons": quick_replies,
                                                                                        },
                                                                                    ]
                                                                                }
                                                                            }
                                                                        }}
                                                                    bot.send_raw(payload)
                                                                # TH3: Không có button quick_replies nhưng lại có ảnh:
                                                                elif not init_bot.next_question_id.selection_answer_ids and init_bot.next_question_id.link_image_url:
                                                                    # Gửi ảnh trước
                                                                    bot.send_image_url(recipient_id=sender_id,
                                                                                       image_url=str(
                                                                                           init_bot.next_question_id.link_image_url))
                                                                    # Sau đó trả lời text
                                                                    bot.send_text_message(sender_id, str(
                                                                        init_bot.next_question_id.question).replace(
                                                                        "user_name", name_user))
                                                                    # log vào lead
                                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        init_bot.next_question_id.question.replace(
                                                                            "user_name",
                                                                            name_user)) if lead.sudo().description else "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        init_bot.next_question_id.question.replace(
                                                                            "user_name", name_user))
                                                                # TH4:       Không có cả ảnh vs các button trả lời nhanh
                                                                elif not init_bot.next_question_id.selection_answer_ids and not init_bot.next_question_id.link_image_url:
                                                                    # Chỉ trả lời mỗi text
                                                                    bot.send_text_message(sender_id, str(
                                                                        init_bot.next_question_id.question).replace(
                                                                        "user_name", name_user))
                                                                    # log vào lead
                                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        init_bot.next_question_id.question.replace(
                                                                            "user_name",
                                                                            name_user)) if lead.sudo().description else "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        init_bot.next_question_id.question.replace(
                                                                            "user_name", name_user))

                                                                else:
                                                                    return
                                                        else:
                                                            # nếu ko tìm đc cả thì trả lời câu hỏi ngoại lệ
                                                            config = request.env[
                                                                'chat.bot.question.and.answer'].sudo().search([],
                                                                                                              limit=1)
                                                            if config:
                                                                if config.exception:
                                                                    bot.send_text_message(sender_id,
                                                                                          str(config.exception).replace(
                                                                                              "user_name", name_user))
                                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        config.exception).replace("user_name",
                                                                                                  name_user) if lead.sudo().description else "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        config.exception).replace("user_name",
                                                                                                  name_user)
                                                else:
                                                    # tim câu trả hỏi chỉ cần map đúng câu trả lời
                                                    init_bot = request.env['prepare.question'].sudo().search(
                                                        [('response_answer', '=', query)], limit=1)
                                                    if init_bot:
                                                        if init_bot:
                                                            if init_bot.next_question_id:
                                                                sender.last_question_id = init_bot.next_question_id
                                                                if init_bot.next_question_id.selection_answer_ids and init_bot.next_question_id.link_image_url:
                                                                    # Trả lời text trước
                                                                    bot.send_text_message(sender_id, str(
                                                                        init_bot.next_question_id.question).replace(
                                                                        "user_name", name_user))
                                                                    # log vào lead
                                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        init_bot.next_question_id.question.replace(
                                                                            "user_name",
                                                                            name_user)) if lead.sudo().description else "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        init_bot.next_question_id.question.replace(
                                                                            "user_name", name_user))
                                                                    # trả lời = template
                                                                    for selection in init_bot.next_question_id.selection_answer_ids:
                                                                        if selection.answer:
                                                                            quick_replies.append({
                                                                                "type": "postback",
                                                                                "title": str(selection.answer).replace(
                                                                                    "user_name", name_user),
                                                                                "payload": "<POSTBACK_PAYLOAD>"
                                                                            })
                                                                    payload = {
                                                                        "recipient": {
                                                                            "id": sender_id
                                                                        },
                                                                        "message": {
                                                                            "attachment": {
                                                                                "type": "template",
                                                                                "payload": {
                                                                                    "template_type": "generic",
                                                                                    "elements": [
                                                                                        {
                                                                                            "title": "Welcome to Flexfit!",
                                                                                            "image_url": str(
                                                                                                init_bot.next_question_id.link_image_url),
                                                                                            "subtitle": "	Xin chào quý khách ghé thăm Flexfit. Chúng tôi có thể giúp gì cho quý khách?",
                                                                                            "default_action": {
                                                                                                "type": "web_url",
                                                                                                "url": "https://flexfit.vn/",
                                                                                                "webview_height_ratio": "tall",
                                                                                            },
                                                                                            "buttons": quick_replies,
                                                                                        },
                                                                                    ]
                                                                                }
                                                                            }
                                                                        }}
                                                                    bot.send_raw(payload)
                                                        else:
                                                            # trường hợp ngoài kịch bản, sẽ lấy câu trả lời ngoại lệ
                                                            config = request.env[
                                                                'chat.bot.question.and.answer'].sudo().search([],
                                                                                                              limit=1)
                                                            if config:
                                                                if config.exception:
                                                                    bot.send_text_message(sender_id,
                                                                                          str(config.exception).replace(
                                                                                              "user_name", name_user))
                                                                    lead.sudo().description = lead.sudo().description + "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        config.exception).replace("user_name",
                                                                                                  name_user) if lead.sudo().description else "\n" + str(
                                                                        datetime.now().astimezone(local_tz).strftime(
                                                                            '%d/%m/%Y %H:%M:%S')) + " Bot: \n\t" + str(
                                                                        config.exception).replace("user_name",
                                                                                                  name_user)
                                except Exception as ex:
                                    a = 0
                                    print(str(ex))
                                    print("Rơi vào ngoại lệ")
        return "ok"
