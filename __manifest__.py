# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Gestión Contratos de Matriculación",
    'summary': "Módulo para la gestión de contratos de estudiantes, materias, profesores y pagos.",
    'description': """
        Este módulo optimiza el proceso de matriculación en una institución educativa,
        permitiendo al personal de control de estudios:
        - Crear contratos de matriculación para cada estudiante.
        - Asociar materias y profesores de forma dinámica, filtrando por la disponibilidad.
        - Asignar costos manuales por materia.
        - Generar facturas automáticamente a partir de los contratos.
        - Obtener un estado de pago automatizado en el contrato, vinculado a la factura generada.
    """,
    'author': "Daniel Canino caninodaniel92@gmail.com",
    'category': 'Education',
    'version': '1.0',
    'depends': [
        'base',
        'account',
        'contacts',
    ],
    'data': [
        # Seguridad
        'security/ir.model.access.csv',
        # Vistas
        'views/educational_contract_views.xml',
        # 'views/account_move_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}