# -*- coding: utf-8 -*-
{
    'name': 'Dashboard_dynamic',
    'version': '',
    'summary': """ Dashboard Dinámico - odoo 18 """,
    'author': '',
    'website': '',
    'category': '',
    'depends': ['base', ],
    "data": [
        "security/ir.model.access.csv",
        "views/dashboard_block_views.xml"
    ],
    
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
