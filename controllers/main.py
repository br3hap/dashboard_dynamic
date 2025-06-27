from odoo import http
from odoo.http import request

class Main(http.Controller):
    
    @http.route('/custom_dashboard/search_input_chart', type='json',
                auth="public", website=True)
    def dashboard_search_input_chart(self, search_input):
        return request.env['dashboard.block'].search([
            ('name', 'ilike', search_input)]).ids
        ...