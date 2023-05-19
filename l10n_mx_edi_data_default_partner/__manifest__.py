# -*- coding: utf-8 -*-

{
    "name": "Uso de cfdi y forma de pago desde cliente",
    "version": "16.0.1.1",
    'author': "InuX",
    'website': "www.google.com",
    'category': '',
    "description": """
           Éste módulo permite predeterminar  un uso de CFDI y forma de pago desde el catálogo de clientes.
           La factura será creada con los valores determinados. (Enterprise)
    """,
    "depends": [
        "account", "l10n_mx_edi", "sale"
    ],
    "data": ['views/res_partner_views.xml',
             'views/account_move_views.xml',
             ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
