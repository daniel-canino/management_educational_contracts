from odoo import models, fields, api


class EducationalSubject(models.Model):
    _name = 'educational.subject'
    _description = 'Materia Educativa'


    name = fields.Char(string='Nombre de la Materia', required=True)
    code = fields.Char(string='Código de la Materia', required=True)
    description = fields.Text(string='Descripción')
    active = fields.Boolean(string='Activo', default=True)
    product_id = fields.Many2one(
        comodel_name='product.product', 
        string='Producto Asociado',
        domain="[('type', '=', 'service')]", 
        required=True
    )