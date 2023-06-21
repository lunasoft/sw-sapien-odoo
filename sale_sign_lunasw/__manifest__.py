# -*- coding: utf-8 -*-

{
    "name": "Sale Sign Luna SW",
    "version": "1.0.0",
    'author': "InuX",
    'website': "www.google.com",
    'category': 'sales',
    "description": """
           Funciones extras para la firma de documentos desde las cotizaciones
    """,
    "depends": [
        "sale_management",
        "sign",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/res_partner_view.xml",
        "data/sign_item_type.xml",
        "data/sign_lunasw_groups.xml",
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
