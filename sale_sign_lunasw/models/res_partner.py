# -*- coding: utf-8 -*-

from odoo import fields, models, api, SUPERUSER_ID, _


class ResPartner(models.Model):
    _inherit = 'res.partner'


    rep_legal = fields.Char('Representante Legal')
    razon_social = fields.Char('Razón Social')
    firmas_count = fields.Integer('Firmas NO.', compute='_compute_firmas_count')

    def _compute_firmas_count(self):
        for record in self:
            firmas_items = self.env['sign.request.item'].search([('partner_id', '=', record.id)])
            docs = self.env['sign.request'].search([('request_item_ids', 'in', firmas_items.ids)])
            record.firmas_count = len(docs.ids)

    def action_view_documentos(self):
        self.ensure_one()
        firmas_items = self.env['sign.request.item'].search([('partner_id', '=', self.id)])
        docs = self.env['sign.request'].search([('request_item_ids', 'in', firmas_items.ids)])
        result = {
            "type": "ir.actions.act_window",
            "res_model": "sign.request",
            "domain": [('id', 'in', docs.ids)],
            "context": {"create": False},
            "name": "Documentos para firma",
            'view_mode': 'tree',
        }
        return result