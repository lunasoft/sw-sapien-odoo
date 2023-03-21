# -*- coding: utf-8 -*-

{
    "name": "CFDI set UUID Sync SAT Mx",
    "version": "1.0",
    'author': "InuX",
    'website': "www.google.com",
    'category': '',
    "description": """
           Éste módulo permite modificar el campo UUID de las facturas para poder cargar saldos iniciales.
           Al usar el Módulo de syncronización con el SAT, tomará este valor
    """,
    "depends": [
        "account",
        "l10n_mx_sat_sync_itadmin_ee",
    ],
    "data": [
        "views/account_move_view.xml",
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
