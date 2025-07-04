# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class DashboardTheme(models.Model):
    _name = 'dashboard.theme'
    _description = 'DashboardTheme'

    name = fields.Char(string='Nombre del tema', help='Nombre del tema')
    color_x = fields.Char(string='Color X', help='Seleccione el color X del tema',
                          default='#4158D0')
    color_y = fields.Char(string='Color Y', help='Seleccione el color Y del tema',
                          default='#C850C0')
    color_z = fields.Char(string='Color Z', help='Seleccione el color Z del tema',
                          default='#FFCC70')
    body = fields.Html(string='Cuerpo', help='Vista Previa del tema')
    style = fields.Char(string='Estilo',
                        help='Estilo')
    

    @api.constrains('name', 'color_x', 'color_y', 'color_z')
    def save_record(self):
        self.body = f"<div style='width:300px; height:300px;background-image: linear-gradient(50deg, {self.color_x} 0%, {self.color_y} 46%, {self.color_z} 100%);'/>"
        self.style = f"background-image: linear-gradient(50deg, {self.color_x} 0%, {self.color_y} 46%, {self.color_z} 100%);"


    def get_records(self):
        records = self.search_read([], ['name', 'style'])
        return records
