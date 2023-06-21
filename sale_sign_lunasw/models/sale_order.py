# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    documentos_ids = fields.One2many('sign.request', 'sale_order_id', 'Docs a Firmar')
    firmas_count = fields.Integer('Firmas NO.', compute='_compute_firmas_count')

    @api.depends('documentos_ids')
    def _compute_firmas_count(self):
        for record in self:
            record.firmas_count = len(record.documentos_ids)

    def lanzar_wizard_firma(self): #contrato Luna
        action = self.env['ir.actions.act_window']._for_xml_id('sign.action_sign_send_request')
        plantilla_id = False
        contrato_tag_id = self.env['sign.template.tag'].search([('name', '=', self.env.context.get('tipo'))], limit=1).id
        for plantilla in self.env['sign.template'].search([]):
            if contrato_tag_id in plantilla.tag_ids.ids:
                plantilla_id = plantilla.id
        if not plantilla_id:
            raise UserError('No se encontró ninguna plantilla de contrato para la compañía')
        action["context"] = {
            "active_id": plantilla_id,
            "sign_directly_without_mail": True,
            "default_sale_order_id": self.id,
        }
        return action

    def action_view_documentos(self):
        self.ensure_one()
        result = {
            "type": "ir.actions.act_window",
            "res_model": "sign.request",
            "domain": [('id', 'in', self.documentos_ids.ids)],
            "context": {"create": False},
            "name": "Documentos para firma",
            'view_mode': 'tree',
        }
        return result