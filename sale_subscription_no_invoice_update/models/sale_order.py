# -*- coding: utf-8 -*-

from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def avanzar_fecha_siguiente_factura(self):
        self._update_next_invoice_date()