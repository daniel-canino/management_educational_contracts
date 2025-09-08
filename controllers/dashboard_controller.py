import odoo
from odoo import http
from odoo.http import request

class PowerBiController(http.Controller):

    @http.route('/get/dashboardparameter', type='json', auth="user")
    def get_dashboard_parameters(self):
        """
        Método para obtener la URL del dashboard de Power BI desde el servidor.
        Este método podría también obtener tokens de seguridad o cualquier otra información necesaria.
        """
        dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiN2UyZDUzZTUtMTZmMi00YjMwLWFlZTEtZTk2NzQ1NjJhZ[%E2%80%A6]6IjBiMTgwYjAyLTIzMTUtNDBjMS05ZWIxLTY0MDk4N2FmNDRkYyIsImMiOjl9"
        
        return {
            'embed_url': dashboard_url,
            'embed_token': 'TOKEN',
            'dashboard_id': 'ID'
        }