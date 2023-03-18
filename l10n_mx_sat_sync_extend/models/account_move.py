# -*- coding: utf-8 -*-

from odoo import fields, models, api, SUPERUSER_ID, _


class AccountMove(models.Model):
    _inherit = 'account.move'


    l10n_mx_edi_cfdi_uuid_cusom = fields.Char(string="UUID de saldo inicial")
    cargar_saldo_inicial = fields.Boolean(string="Saldo inicial", related='journal_id.cargar_saldo_inicial')

    @api.depends('edi_document_ids')
    def _compute_cfdi_values(self):
        '''Fill the invoice fields from the cfdi values. #original function overwritten!
        '''
        for move in self:
            cfdi_infos = move._l10n_mx_edi_decode_cfdi()

            move.l10n_mx_edi_cfdi_uuid = cfdi_infos.get('uuid', move.cargar_saldo_inicial and move.l10n_mx_edi_cfdi_uuid_cusom or False)
            move.l10n_mx_edi_cfdi_supplier_rfc = cfdi_infos.get('supplier_rfc')
            move.l10n_mx_edi_cfdi_customer_rfc = cfdi_infos.get('customer_rfc')
            move.l10n_mx_edi_cfdi_amount = cfdi_infos.get('amount_total')


class AccountJournal(models.Model):
    _inherit = 'account.journal'


    cargar_saldo_inicial = fields.Boolean(string="Permitir cargar saldos iniciales")