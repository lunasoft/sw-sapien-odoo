# -*- coding: utf-8 -*-

from odoo import fields, models, api, SUPERUSER_ID, _
import logging

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'


    def regenerar_polizas_outstanding(self):
        '''Se llamará desde un cron
        '''
        cuentas_outstanding = self.env['account.account'].search([('name', 'ilike', '%outstanding%')])
        cuentas_ids = cuentas_outstanding.ids
        apuntes = self.search([('account_id', 'in', cuentas_ids), ('parent_state', '!=', 'cancel')])
        _logger.info("Cuentas a corregir: %s"%len(apuntes))
        i = 1
        for move in apuntes:
            cuenta_ok_id = move.journal_id.default_account_id.id
            query = "UPDATE account_move_line SET account_id = %s WHERE id=%s" % (cuenta_ok_id, move.id)
            self._cr.execute(query)
            if i % 100 == 0:
                _logger.info("Proceso: %s de %s"%(i, len(apuntes)))
            i+=1
        _logger.info("Proceso terminó exitosamente")