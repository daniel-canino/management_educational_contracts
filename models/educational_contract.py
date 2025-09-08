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
        string='Líneas del Contrato',
        required=True,
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


    @api.depends('contract_line_ids.cost')
    def _compute_total_amount(self):
        for contract in self:
            contract.total_amount = sum(line.cost for line in contract.contract_line_ids)


class EducationalContractLine(models.Model):
    _name = 'educational.contract.line'
    _description = 'Línea del Contrato de Matriculación'


    contract_id = fields.Many2one(
        comodel_name='educational.contract', 
        string='Contrato', 
        ondelete='cascade'
    )
    student_subject_ids = fields.Many2many(related='contract_id.student_id.student_subject_ids')
    subject_id = fields.Many2one(
        comodel_name='educational.subject', 
        string='Materia', 
        domain="[('active', '=', True), ('id', 'in', student_subject_ids)]", 
        required=True
    )
    professor_subject_ids = fields.Many2many(related='subject_id.professor_subject_ids')
    professor_id = fields.Many2one(
        comodel_name='res.partner', 
        string='Profesor', 
        domain="[('is_professor', '=', True), ('id', 'in', professor_subject_ids)]", 
        required=True
    )
    cost = fields.Float(string='Costo', required=True)