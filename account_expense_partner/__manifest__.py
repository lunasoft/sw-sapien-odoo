# -*- coding: utf-8 -*-

{
    "name": "Cuenta de Gastos por Proveedor",
    "version": "1.0.0",
    'author': "Morfosys",
    'website': "www.google.com",
    'category': 'accounting',
    "description": """
           Agrega funcionalidad para configurar las cuentas de gastos por proveedor
    """,
    "depends": [
        "account",
    ],
    "data": [
        "views/res_partner.xml",
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
