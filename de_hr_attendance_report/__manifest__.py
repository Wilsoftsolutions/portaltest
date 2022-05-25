# -*- coding: utf-8 -*-
{
    'name': "Attendance Report",

    'summary': """
            Attendance Report
        """,

    'description': """
        Attendance Report
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Attendance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_attendance','de_hr_attendance_approvals'],

    # always loaded
    'data': [
        'wizard/hr_attendance_report_wizard.xml',
        'report/hr_attendance_report.xml',
        'views/hr_attendance_views.xml',   
        'report/hr_attendance_report_template.xml',
        'security/ir.model.access.csv',
        'views/hr_attendance_report_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

