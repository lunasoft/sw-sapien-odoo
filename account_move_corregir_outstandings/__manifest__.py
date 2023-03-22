# -*- coding: utf-8 -*-

{
    "name": "Corregir polizas outstanding por migracion",
    "version": "1.0",
    'author': "InuX",
    'website': "www.google.com",
    'category': '',
    "description": """
           Éste módulo corrige las pólizas por el cambio a oustanding en las versiones 16
           Coloca la cuenta configurada en el diario.
    """,
    "depends": [
        "account",
    ],
    "data": [
        'data/cron_data.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
