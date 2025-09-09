from odoo import models, fields, api
from datetime import date, timedelta


class EducationalContract(models.Model):
    _name = 'educational.contract'
    _description = 'Contrato de Matriculación'


    name = fields.Char(string='Número de Contrato', copy=False, readonly=True)
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
    )
    total_amount = fields.Float(string='Monto Total', compute='_compute_total_amount', store=True)
    invoice_ids = fields.One2many(
        comodel_name='account.move',
        inverse_name='educational_contract_id', 
        string='Factura Asociada', 
        readonly=True
    )
    has_invoice = fields.Boolean(compute="_compute_has_invoice", store=True)
    payment_status = fields.Selection(
        selection=[
            ('nothing', 'Nada que pagar'),
            ('not_paid', 'No pagado'),
            ('in_payment', 'En proceso'),
            ('paid', 'Pagado'),
            ('partial', 'Parcialmente pagado'),
            ('reversed', 'Revertido'),
        ],
        string='Estado de Pago',
        compute='_compute_payment_status',
        store=True
    )

    # ORM METHODS #
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('educational.contract') or "Nuevo"

        return super().create(vals_list)
    
    # COMPUTE METHODS #
    @api.depends('contract_line_ids.cost')
    def _compute_total_amount(self):
        for contract in self:
            contract.total_amount = sum(line.cost for line in contract.contract_line_ids)

    @api.depends('invoice_ids')
    def _compute_has_invoice(self):
        for contract in self:
            contract.has_invoice = bool(contract.invoice_ids)

            
    @api.depends('invoice_ids.payment_state')
    def _compute_payment_status(self):
        payment_map = {
            'not_paid': 'not_paid',
            'in_payment': 'in_payment',
            'paid': 'paid',
            'partial': 'partial',
            'reversed': 'reversed'
        }
        for contract in self:
            if not contract.invoice_ids:
                contract.payment_status = 'nothing'
            else:
                invoice = contract.invoice_ids[0]
                contract.payment_status = payment_map.get(invoice.payment_state, 'not_paid')

    # ACTION METHODS #
    def action_create_invoice(self):
        self.ensure_one()
        if self.invoice_ids:
            raise models.ValidationError("Ya existe una factura asociada a este contrato.")

        if not self.contract_line_ids:
            raise models.ValidationError("El contrato debe tener al menos una línea.")
        
        invoice_line_vals = []
        for line in self.contract_line_ids:
            if line.cost <= 0:
                raise models.ValidationError(f"El costo de la materia '{line.subject_id.name}' debe ser mayor que cero.")
            
            if not line.subject_id.product_id:
                raise models.ValidationError(f"La materia '{line.subject_id.name}' no tiene un producto asociado.")
            
            invoice_line_vals.append((0, 0, {
                'name': f"{line.subject_id.name} - Profesor: {line.professor_id.name}",
                'quantity': 1,
                'price_unit': line.cost,
                'product_id': line.subject_id.product_id.id,
            }))

        invoice_date = date.today()
        vals = {
            'move_type': 'out_invoice',
            'partner_id': self.student_id.id,
            'educational_contract_id': self.id,
            'invoice_line_ids': invoice_line_vals,
            'invoice_date': invoice_date,
            'invoice_origin': self.name
        }
        self.env['account.move'].create(vals)
    

    def action_open_invoice(self):
        self.ensure_one()
        if not self.invoice_ids:
            raise models.ValidationError("No hay factura asociada a este contrato.")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Factura',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_ids[0].id,
            'target': 'current',
        }
    
    
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