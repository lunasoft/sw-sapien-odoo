# -*- coding: utf-8 -*-

from odoo import api, models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_mx_edi_usage = fields.Selection(
        selection=[
            ('G01', 'Adquisición de mercancías'),
            ('G02', 'Devoluciones, descuentos o bonificaciones'),
            ('G03', 'Gastos en general'),
            ('I01', 'Construcciones'),
            ('I02', 'Mobiliario y equipo de oficina por inversiones'),
            ('I03', 'Equipo de transporte'),
            ('I04', 'Equipo de computo y accesorios'),
            ('I05', 'Dados, troqueles, moldes, matrices y herramental'),
            ('I06', 'Comunicaciones telefónicas'),
            ('I07', 'Comunicaciones satelitales'),
            ('I08', 'Otra maquinaria y equipo'),
            ('D01', 'Honorarios médicos, dentales y gastos hospitalarios'),
            ('D02', 'Gastos médicos por incapacidad o discapacidad'),
            ('D03', 'Gastos funerales'),
            ('D04', 'Donativos'),
            ('D05', 'Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)'),
            ('D06', 'Aportaciones voluntarias al SAR'),
            ('D07', 'Primas por seguros de gastos médicos'),
            ('D08', 'Gastos de transportación escolar obligatoria'),
            ('D09', 'Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones'),
            ('D10', 'Pagos por servicios educativos (colegiaturas)'),
            ('S01', "Sin Efectos Fiscales")], default=False,
        string="Uso CFDI predeterminado")

    l10n_mx_edi_payment_method_id = fields.Many2one(
        comodel_name='l10n_mx_edi.payment.method',
        string="Forma de Pago predeterminada")