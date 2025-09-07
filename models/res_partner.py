from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    is_student = fields.Boolean(string='Es Estudiante', default=False)
    is_professor = fields.Boolean(string='Es Profesor', default=False)
    student_contract_ids = fields.One2many(
        comodel_name='educational.contract',
        inverse_name='student_id',
        string='Contratos de Matriculación'
    )
    professor_subject_ids = fields.Many2many(
        comodel_name='educational.subject',
        relation='professor_subject_rel',
        column1='professor_id',
        column2='subject_id',
        string='Materias que imparte'
    )