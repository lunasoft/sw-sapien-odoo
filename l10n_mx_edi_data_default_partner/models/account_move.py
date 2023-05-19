# -*- coding: utf-8 -*-

from odoo import api, models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_mx_edi_forzar_politica = fields.Selection(string='Forzar política de pago', selection=[('PPD', 'PPD'), ('PUE', 'PUE')])
    l10n_mx_edi_usage = fields.Selection(selection_add=[], default=lambda self: self.partner_id.l10n_mx_edi_usage)

    def _compute_l10n_mx_edi_payment_method_id(self):
        for move in self:
            if move.partner_id and move.partner_id.l10n_mx_edi_payment_method_id:
                move.l10n_mx_edi_payment_method_id = move.partner_id.l10n_mx_edi_payment_method_id.id
            else:
                super(AccountMove, self)._compute_l10n_mx_edi_payment_method_id()

    def _compute_l10n_mx_edi_payment_policy(self):
        for move in self:
            if move.l10n_mx_edi_forzar_politica:
                move.l10n_mx_edi_payment_policy = move.l10n_mx_edi_forzar_politica
            else:
                super(AccountMove, self)._compute_l10n_mx_edi_payment_policy()