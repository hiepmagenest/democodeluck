# -*- coding: utf-8 -*-
{
    'name': "Facebook Get Comments Live Stream",

    'summary': """
        FACEBOOK GET COMMENT LIVE STREAM
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Magenest",
    'website': "https://magenest.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'wizards/fetch_info_pages.xml',

        'views/facebook_page.xml',
        'views/facebook_page_category.xml',
        # 'views/live_stream.xml',
        'views/live_videos.xml',
        'views/facebook_comment.xml',
        'views/facebook_user.xml',

        'views/contacts_fb.xml',
        'views/crm_fb.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
