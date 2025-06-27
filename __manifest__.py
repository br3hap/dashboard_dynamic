# -*- coding: utf-8 -*-
{
    'name': 'Dashboard Dinámicos',
    'version': '1.0',
    'summary': """ Dashboard Dinámico - odoo 18 """,
    'author': 'Breithner Aquituari',
    'website': '',
    'category': '',
    'depends': ['web', ],
    "data": [
        "security/ir.model.access.csv",
        "data/dashboard_theme_data.xml",
        "views/dashboard_views.xml",
        "views/dashboard_block_views.xml",
        "views/dashboard_theme_views.xml"
    ],

    'assets': {
        'web.assets_backend': [
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js',
            'dashboard_dynamic/static/src/css/**/*.css',
            'dashboard_dynamic/static/src/scss/**/*.scss',
            'dashboard_dynamic/static/src/js/**/*.js',
            'dashboard_dynamic/static/src/xml/**/*.xml',
            'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css',
            'dashboard_dynamic/static/src/js/interact_min.js'
        ],
    },
    
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
