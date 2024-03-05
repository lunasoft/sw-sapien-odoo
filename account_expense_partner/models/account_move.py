# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('display_type', 'company_id', 'partner_id')
    def _compute_account_id(self):
        for line in self:
            if line.product_id and line.move_id.is_purchase_document(include_receipts=True) and\
                line.display_type not in ('line_section', 'line_note') and line.partner_id.property_account_expense_id:
                    line.account_id = line.partner_id.property_account_expense_id.id
            else:
                super(AccountMoveLine, line)._compute_account_id()