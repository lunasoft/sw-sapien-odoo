# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    forzar_date = fields.Boolean('Forzar Fecha al Periodo', default=True)

    def reverse_moves(self):
        if self.forzar_date:
            self.date_mode = 'entry'
        action = super(AccountMoveReversal, self).reverse_moves()
        fecha = False
        #for refund in self.new_move_ids:
        #    for move in self.move_ids:
        #        fecha = move.date
        #        break
        #    refund.date = fecha
        return action