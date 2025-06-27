# -*- coding: utf-8 -*-
import logging
from ast import literal_eval

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression

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
        block_id = []
        for rec in self.env['dashboard.block'].sudo().search(
                [('client_action_id', '=', int(action_id))]):
            if rec.filter is False:
                rec.filter = "[]"
            filter_list = literal_eval(rec.filter)
            filter_list = [filter_item for filter_item in filter_list if not (
                    isinstance(filter_item, tuple) and filter_item[
                0] == 'create_date')]
            rec.filter = repr(filter_list)
            vals = {'id': rec.id, 'name': rec.name, 'type': rec.type,
                    'graph_type': rec.graph_type, 'icon': rec.fa_icon,
                    'model_name': rec.model_name,
                    'color': f'background-color: {rec.tile_color};' if rec.tile_color else '#1f6abb;',
                    'text_color': f'color: {rec.text_color};' if rec.text_color else '#FFFFFF;',
                    'val_color': f'color: {rec.val_color};' if rec.val_color else '#FFFFFF;',
                    'icon_color': f'color: {rec.tile_color};' if rec.tile_color else '#1f6abb;',
                    'height': rec.height,
                    'width': rec.width,
                    'translate_x': rec.translate_x,
                    'translate_y': rec.translate_y,
                    'data_x': rec.data_x,
                    'data_y': rec.data_y,
                    'domain': filter_list,
                    }
            domain = []
            if rec.filter:
                domain = expression.AND([literal_eval(rec.filter)])
            if rec.model_name:
                if rec.type == 'graph':
                    self._cr.execute(self.env[rec.model_name].get_query(domain,
                                                                        rec.operation,
                                                                        rec.measured_field_id,
                                                                        start_date,
                                                                        end_date,
                                                                        group_by=rec.group_by_id))
                    records = self._cr.dictfetchall()
                    x_axis = []
                    for record in records:
                        if record.get('name') and type(
                                record.get('name')) == dict:
                            x_axis.append(record.get('name')[self._context.get(
                                'lang') or 'en_US'])
                        else:
                            x_axis.append(record.get(rec.group_by_id.name))
                    y_axis = []
                    for record in records:
                        y_axis.append(record.get('value'))
                    vals.update({'x_axis': x_axis, 'y_axis': y_axis})
                else:
                    self._cr.execute(self.env[rec.model_name].get_query(domain,
                                                                        rec.operation,
                                                                        rec.measured_field_id,
                                                                        start_date,
                                                                        end_date))
                    records = self._cr.dictfetchall()
                    magnitude = 0
                    total = records[0].get('value')
                    while abs(total) >= 1000:
                        magnitude += 1
                        total /= 1000.0
                    val = '%.2f%s' % (
                        total, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
                    records[0]['value'] = val
                    vals.update(records[0])
            block_id.append(vals)
        return block_id