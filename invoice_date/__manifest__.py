# -*- coding: utf-8 -*-
{
    'name': "Product Quantity By Color &amp; Size",

    'summary': """This is module is used to show the quantity of 
    the product regarding size""",

    'description': """
        This is module is used to show the quantity of 
    the product regarding size
    """,

    'author': "sadnan khan",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'product', 'account', 'sale'],

    # always loaded
    'data': [
        'invoice_report/report.xml',
        'invoice_report/sale_delivery_report_action.xml',
        'invoice_report/report_template.xml',
        'invoice_report/sale_delivery_report.xml',
        'invoice_report/delivery_header.xml',
        'invoice_report/footer.xml',
        'invoice_report/header.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
