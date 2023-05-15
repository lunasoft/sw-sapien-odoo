# -*- coding: utf-8 -*-

from odoo import api, models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_mx_edi_forzar_politica = fields.Selection(string='Forzar política de pago', selection=[('PPD', 'PPD'), ('PUE', 'PUE')])

    def _compute_l10n_mx_edi_payment_method_id(self):
        for move in self:
            if move.partner_id and move.partner_id.l10n_mx_edi_payment_method_id:
                move.l10n_mx_edi_payment_method_id = move.partner_id.l10n_mx_edi_payment_method_id.id
            else:
                super(AccountMove, self)._compute_l10n_mx_edi_payment_method_id()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            partner = 'partner_id' in vals and self.env['res.partner'].browse(vals['partner_id'])
            if partner and partner.l10n_mx_edi_usage:
                vals['l10n_mx_edi_usage'] = partner.l10n_mx_edi_usage
        return super(AccountMove, self).create(vals_list)

    def _compute_l10n_mx_edi_payment_policy(self):
        for move in self:
            if move.l10n_mx_edi_forzar_politica:
                move.l10n_mx_edi_payment_policy = move.l10n_mx_edi_forzar_politica
            else:
                super(AccountMove, self)._compute_l10n_mx_edi_payment_policy()