from odoo import models, fields, api, _
import requests
import json
from odoo.exceptions import ValidationError


class FetchInfoPages(models.TransientModel):
    _name = "fetch.info.pages"

    fb_user_id = fields.Char(string=_("Facebook User ID"))
    user_accesss_token = fields.Char(string=_("User Token In APP"))

    def action_all_access_token(self):
        user_id = self.fb_user_id
        user_token = self.user_accesss_token
        try:
            if user_id and user_token:
                request_url = "https://graph.facebook.com/v9.0/" + \
                              str(user_id) + "/" + "accounts" + "?" + \
                              "fields=name,category,access_token&" + "access_token=" + str(user_token)
                req = requests.get(request_url)
                if req.status_code >= 200 and req.status_code < 300:
                    content = req.json()
                    if content:
                        for rec in content['data']:
                            page = self.env['facebook.page'].search([('page_id', '=', rec['id'])], limit=1)
                            name_page = rec['name'].replace(" ", "-")
                            link_url = "https://www.facebook.com/" + name_page + "-" + rec['id']

                            page_category = self.env['facebook.page.category'].search(
                                [('category_name', '=', rec['category'])], limit=1)

                            # Cap nhap ban ghi khi page da ton tai
                            if page:
                                if page_category:
                                    page.update({
                                        'page_access_token': rec['access_token'],
                                        'page_name': rec['name'],
                                        'page_category': page_category.id,
                                        'page_url': link_url,
                                    })
                                else:
                                    new_category = self.env['facebook.page.category'].create({
                                        'category_name': rec['category']
                                    })

                                    page.update({
                                        'page_access_token': rec['access_token'],
                                        'page_name': rec['name'],
                                        'page_category': new_category.id,
                                        'page_url': link_url,
                                    })
                            # Tao moi thong tin tu page fetch ve
                            else:
                                if page_category:
                                    new_page = self.env['facebook.page'].create({
                                        'page_access_token': rec['access_token'],
                                        'page_id': rec['id'],
                                        'page_name': rec['name'],
                                        'page_category': page_category.id,
                                        'page_url': link_url,
                                    })
                                else:
                                    new_category = self.env['facebook.page.category'].create({
                                        'category_name': rec['category']
                                    })

                                    new_page = self.env['facebook.page'].create({
                                        'page_access_token': rec['access_token'],
                                        'page_id': rec['id'],
                                        'page_name': rec['name'],
                                        'page_category': new_category.id,
                                        'page_url': link_url,
                                    })

                        # xoa ban ghi rong
                        empty_record = self.env['facebook.page'].sudo().search([('page_id', '=', False)])
                        if empty_record:
                            empty_record.unlink()
                        action = self.env.ref('sim_facebook_live_stream.facebook_page_list_view').read()[0]
                        return action
                else:
                    error_msg = "Client Response " + str(req.status_code)
                    raise ValidationError(error_msg)

        except Exception as e:
            raise ValidationError(_('Error : %s', e))
