# -*- coding: utf-8 -*-

from odoo import api, models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        print(vals)
        if self.partner_id.l10n_mx_edi_usage:
            vals['l10n_mx_edi_usage'] = self.partner_id.l10n_mx_edi_usage
        return vals