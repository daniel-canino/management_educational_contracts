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
        string='Servicio Asociado',
        domain="[('type', '=', 'service')]", 
    )
    professor_subject_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='professor_subject_rel',
        column1='subject_id',
        column2='professor_id',
        string='Profesores que imparten',
        domain="[('is_professor', '=', True)]"
    )
    student_subject_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='student_subject_rel',
        column1='subject_id',
        column2='student_id',
        string='Estudiantes inscritos',
        domain="[('is_student', '=', True)]"
    )

    # ACTION METHODS #
    def action_create_product(self):
        self.ensure_one()
        if not self.product_id:
            product = self.env['product.product'].create({
                'name': self.name,
                'detailed_type': 'service',
                'default_code': self.code,
            })
            self.product_id = product


    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            if self.search_count([('code', '=', record.code), ('id', '!=', record.id)]) > 0:
                raise models.ValidationError(f"El código '{record.code}' ya está en uso. Debe ser único.")
                