# -*- coding: utf-8 -*-

{
    "name": "Manual Update Next Invoice Subscription",
    "version": "1.0.0",
    'author': "InuX",
    'website': "www.google.com",
    'category': 'sales',
    "description": """
           Agrega un botón que avanza la fecha de siguiente factura de la subscripción según la periodicidad
    """,
    "depends": [
        "sale_subscription",
    ],
    "data": [
        "views/sale_order_view.xml",
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
