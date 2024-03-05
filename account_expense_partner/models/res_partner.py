# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_account_expense_id = fields.Many2one('account.account', company_dependent=True,
                    string="Cuenta de Gastos", domain="[('account_type', '=', 'expense'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
                    help="Esta cuenta será usada como cuenta de gastos en lugar de la predeterminada y de la cuenta por pagar si está establecida", required=False)