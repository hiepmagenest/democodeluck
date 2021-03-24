# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kanak Infosystems LLP. (<https://www.kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.kanakinfosystems.com/license>
#################################################################################

{
    "name": "Purchase Approval Rules",
    "summary": "Purchase Approval Rules",
    "description": "Purchase Approval Rules",
    'summary': 'Purchase order approval rules',
    "version": "1.0",
    "category": "Purchases",
    "license": "OPL-1",
    "website": "https://www.kanakinfosystems.com",
    "author": "Kanak Infosystems LLP.",
    "depends": ["hr", "purchase"],
    'images': ['static/description/banner.jpg'],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "views/approval_config.xml",
        "views/purchase_order_config.xml",
        "views/purchase_view.xml",
        "wizard/custom_warning_view.xml"
    ],
    'sequence': 1,
    "installable": True,
    "price": 30,
    "currency": "EUR",
}
