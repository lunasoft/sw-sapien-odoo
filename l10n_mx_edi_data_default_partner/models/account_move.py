# -*- coding: utf-8 -*-

from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_mail_template(self):
        """
        :return: the correct mail template baseda en grupo
        """
        usuario = self.env.user
        if usuario.has_group('account_move_corregir_outstandings.group_usar_plantilla_sw'):
            plantilla_sw = self.env['mail.template'].search([('name', '=', 'Factura SW')])
            if plantilla_sw:
                return '__export__.mail_template_77_9d708080' #produccion
                #return '__export__.mail_template_77_c2ae9992' #stag
        else:
            return super(AccountMove, self)._get_mail_template()