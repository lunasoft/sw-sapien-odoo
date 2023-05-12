# -*- coding: utf-8 -*-

from odoo import api, models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _compute_l10n_mx_edi_payment_method_id(self):
        for move in self:
            if move.partner_id and move.partner_id.l10n_mx_edi_payment_method_id:
                move.l10n_mx_edi_payment_method_id = move.partner_id.l10n_mx_edi_payment_method_id.id
                print('encontre')
            else:
                print('no encontre')
                super(AccountMove, self)._compute_l10n_mx_edi_payment_method_id(move)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            partner = 'partner_id' in vals and self.env['res.partner'].browse(vals['partner_id'])
            if partner and partner.l10n_mx_edi_usage:
                vals['l10n_mx_edi_usage'] = partner.l10n_mx_edi_usage
        return super(AccountMove, self).create(vals_list)