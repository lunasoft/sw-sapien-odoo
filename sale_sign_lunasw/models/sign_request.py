# -*- coding: utf-8 -*-

from odoo import fields, models, api, SUPERUSER_ID, _


class SignRequest(models.Model):
    _inherit = 'sign.request'

    sale_order_id = fields.Many2one('sale.order', 'Orden de venta')