from odoo import models, fields, api



class EducationalContract(models.Model):
    _name = 'educational.contract'
    _description = 'Contrato de Matriculación'


    name = fields.Char(string='Número de Contrato', required=True, copy=False, readonly=True)
    student_id = fields.Many2one(
        comodel_name='res.partner', 
        string='Estudiante', 
        domain="[('is_student', '=', True)]", 
        required=True
    )
    contract_line_ids = fields.One2many(
        comodel_name='educational.contract.line',
        inverse_name='contract_id',
        string='Líneas del Contrato'
    )
    total_amount = fields.Float(string='Monto Total', compute='_compute_total_amount', store=True)
    invoice_ids = fields.One2many(
        comodel_name='account.move',
        inverse_name='educational_contract_id', 
        string='Factura Asociada', 
        readonly=True
    )
    payment_status = fields.Selection(
        selection=[
            ('unpaid', 'No Pagado'),
            ('partial', 'Parcialmente Pagado'),
            ('paid', 'Pagado')
        ],
        string='Estado de Pago',
        compute='_compute_payment_status',
        store=True
    )


class EducationalContractLine(models.Model):
    _name = 'educational.contract.line'
    _description = 'Línea del Contrato de Matriculación'


    contract_id = fields.Many2one(
        comodel_name='educational.contract', 
        string='Contrato', 
        ondelete='cascade'
    )
    subject_id = fields.Many2one(
        comodel_name='educational.subject', 
        string='Materia', 
        domain="[('active', '=', True)]", 
        required=True
    )
    professor_id = fields.Many2one(
        comodel_name='res.partner', 
        string='Profesor', 
        domain="[('is_professor', '=', True)]", 
        required=True
    )
    cost = fields.Float(string='Costo', required=True)