from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'


    educational_contract_id = fields.Many2one(
        comodel_name='educational.contract', 
        string='Contrato de Matriculación', 
        readonly=True
    )