# -*- coding: utf-8 -*-

{
    "name": "Plantillas de Distribución Analítica",
    "version": "1.0.0",
    'author': "Morfosys",
    'website': "www.google.com",
    'category': 'accounting',
    "description": """
           Agrega funcionalidad para crear y actualizar la contabilidad analítica en base a plantillas
    """,
    "depends": [
        "analytic",
        "account",
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/ir_rule_data.xml',
        "views/account_analityc_distribution_template.xml",
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
