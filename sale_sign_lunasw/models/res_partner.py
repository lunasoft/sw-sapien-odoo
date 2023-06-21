# -*- coding: utf-8 -*-

from odoo import fields, models, api, SUPERUSER_ID, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    rep_legal = fields.Char('Representante Legal')
    razon_social = fields.Char('Razón Social')