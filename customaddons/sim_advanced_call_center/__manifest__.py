# -*- coding: utf-8 -*-
{
    'name': "advanced_call_center",

    'summary': """CALL API""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Magenest",
    'website': "https://store.magenest.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sh@dowWalker',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'static/src/xml/customer_call_info.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        "static/src/xml/customer_call_info.xml",
    ],
}
