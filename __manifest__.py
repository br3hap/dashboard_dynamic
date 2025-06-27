# -*- coding: utf-8 -*-
{
    'name': 'Dashboard Dinámicos',
    'version': '1.0',
    'summary': """ Dashboard Dinámico - odoo 18 """,
    'author': 'Breithner Aquituari',
    'website': '',
    'category': '',
    'depends': ['base', ],
    "data": [
        "security/ir.model.access.csv",
        "views/dashboard_block_views.xml",
        "views/dashboard_theme_views.xml"
    ],
    
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
