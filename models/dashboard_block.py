# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class DashboardBlock(models.Model):
    _name = 'dashboard.block'
    _description = 'DashboardBlock'


    def get_default_action(self):
        action_id = self.env.ref(
            'dashboard_dynamic.dashboard_view_action')
        if action_id:
            return action_id.id
        return False

    name = fields.Char('Nombre del bloque')
    fa_icon = fields.Char(string=_('Icono'))
    operation = fields.Selection(
        string=_('Operación'),
        selection=[
            ('sum', 'Suma'),
            ('avg', 'Promedio'),
            ('count', 'Conteo'),
        ],
        required=True
    )
    graph_type = fields.Selection(
        string=_('Tipo de Gráfico'),
        selection=[
            ('bar', 'Bar'),
            ('radar', 'Radar'),
            ('pie', 'Pie'),
            ('polarArea', 'Polar Area'),
            ('line', 'Line'),
            ('doughnut', 'Doughnut'),
        ],
    )
    measured_field_id = fields.Many2one('ir.model.fields', string='Campo medido')
    client_action_id = fields.Many2one('ir.actions.client', string='Acción de cliente', default=get_default_action)
    type = fields.Selection(
        string=_('Tipo'),
        selection=[
            ('graph', 'Chart'),
            ('tile', 'Tile'),
        ],
    )
    x_axis = fields.Char(string=_('X-Axis'))
    y_axis = fields.Char(string=_('Y-Axis'))
    height = fields.Char(string=_('Height'))
    width = fields.Char(string=_('Width'))
    translate_x = fields.Char(string=_('Translate X'))
    translate_y = fields.Char(string=_('Translate Y'))
    data_x = fields.Char(string=_('Data X'))
    data_y = fields.Char(string=_('Data Y'))
    data_y = fields.Char(string=_('Data Y'))
    group_by_id = fields.Many2one('ir.model.fields', string='Group by (Y- Axis)')
    tile_color = fields.Char(string=_('Tile Color'))
    text_color = fields.Char(string=_('Text Color'))
    val_color = fields.Char(string=_('Valor del Color'))
    fa_color = fields.Char(string=_('Icono del Color'))
    filter = fields.Char(string=_('Filter'))
    model_id = fields.Many2one('ir.model', string='Model')
    model_name = fields.Char(related='model_id.model' ,string=_('Nombre del modelo'))
    edit_mode = fields.Boolean(string=_('Modo editar'))


    
    @api.onchange('model_id')
    def _onchange_model_id(self):
        if self.operation or self.measured_field_id:
            self.operation = False
            self.measured_field_id = False
            self.group_by_id = False


    def get_save_layout(self, grid_data_list):
        for data in grid_data_list:
            block = self.browse(int(data['id']))
            if data.get('data-x'):
                block.write({
                    'translate_x': f"{data['data-x']}px",
                    'translate_y': f"{data['data-y']}px",
                    'data_x': data['data-x'],
                    'data_y': data['data-y'],
                })
            if data.get('height'):
                block.write({
                    'height': f"{data['height']}px",
                    'width': f"{data['width']}px",
                })
        return True
    

    def get_dashboard_vals(self, action_id, start_date=None, end_date=None):
        pass