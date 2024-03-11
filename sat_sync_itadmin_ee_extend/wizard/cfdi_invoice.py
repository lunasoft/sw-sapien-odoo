# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class CfdiInvoiceAttachment(models.TransientModel):
    _inherit = 'cfdi.invoice.attachment'


    @api.model
    def get_or_create_product(self, default_code, product_name, clave_unidad, unit_price, clave_producto, sale_ok=True, purchase_ok=False):
        product_exist = False
        product_obj = self.env['product.product']
        product_types = dict(product_obj._fields.get('type')._description_selection(product_obj.env))
        product_type_default = self.env['ir.config_parameter'].sudo().get_param('l10n_mx_sat_sync_itadmin_ee.product_type_default')
        p_supplierinfo = self.env['product.supplierinfo']
        if default_code:
            product_exist = product_obj.search([('default_code', '=', default_code)], limit=1)
            if not product_exist:
                supplierinfo_exist = p_supplierinfo.search([('product_code', '=', default_code)], limit=1)
                if supplierinfo_exist.product_tmpl_id:
                    product_exist = supplierinfo_exist.product_tmpl_id.product_variant_id
        if not product_exist:
            product_exist = product_obj.search([('name', '=', product_name)], limit=1)
        if not product_exist and self.si_producto_no_tiene_codigo == 'Buscar manual': #llama funcion original que regresará el manual
            product_exist = super(CfdiInvoiceAttachment, self).get_or_create_product(default_code, product_name, clave_unidad, unit_price, clave_producto, sale_ok, purchase_ok)
        sat_code = self.env['product.unspsc.code'].search([('code', '=', clave_producto)], limit=1)
        if not product_exist:  # se agrega buscar por codigo
            if not sat_code:
                raise UserError("No tiene configurada la clave del SAT %s. Por favor configure la clave primero" % (clave_producto))
            product_exist = product_obj.search([('unspsc_code_id', '=', sat_code.id)], limit=1)
        if not product_exist:
            um_descripcion = self.env['uom.uom'].search([('unspsc_code_id.code','=',clave_unidad)], limit=1)
            if not um_descripcion:
                raise UserError("No tiene configurada la unidad de medida %s. Por favor configure la unidad de medida primero"%(clave_unidad))
            product_vals = {'default_code': sat_code.code, 'name': sat_code.name, 'standard_price': unit_price,
                            'uom_id': um_descripcion.id, 'unspsc_code_id': sat_code.id, 'uom_po_id': um_descripcion.id,
                            'description': 'Nombre asignado por el proveedor: ' + str(product_name), 'sale_ok': sale_ok, 'purchase_ok': purchase_ok}
            if product_type_default:
                product_vals.update({'type': product_type_default})
            elif 'product' in product_types:
                product_vals.update({'type': 'product'})
            product_exist = product_obj.create(product_vals)

        return product_exist

    @api.model
    def get_tax_from_codes(self, taxes, tax_type, no_imp_tras):
        tax_codes = {'001': 'ISR', '002': 'IVA', '003': 'IEPS'}
        tax_obj = self.env['account.tax']
        tax_ids = []
        if taxes:
            k = 0
            for tax in taxes:
                if tax.get('@TasaOCuota'):
                    if k < no_imp_tras:
                        amount_tasa = float(tax.get('@TasaOCuota')) * 100
                    else:
                        amount_tasa = float(tax.get('@TasaOCuota')) * -100
                    tasa = str(amount_tasa)
                else:
                    tasa = str(0)

                tax_exist = tax_obj.search(
                    [('type_tax_use', '=', tax_type), ('l10n_mx_tax_type', '=', tax.get('@TipoFactor')),
                     ('amount', '=', tasa), ('company_id', '=', self.env.company.id)], limit=1)
                if not tax_exist:
                    lim_menor = str(float(tasa)-0.1)
                    lim_mayor = str(float(tasa)+0.1)
                    tax_exist = tax_obj.search( #para numeros positivos
                        [('type_tax_use', '=', tax_type), ('l10n_mx_tax_type', '=', tax.get('@TipoFactor')),
                         ('amount', '>', lim_menor), ('amount', '<', lim_mayor), ('company_id', '=', self.env.company.id)], limit=1)
                    if not tax_exist:
                        tax_exist = tax_obj.search(  # para numeros negativos
                            [('type_tax_use', '=', tax_type), ('l10n_mx_tax_type', '=', tax.get('@TipoFactor')),
                             ('amount', '>', lim_mayor), ('amount', '<', lim_menor),
                             ('company_id', '=', self.env.company.id)], limit=1)
                tax_ids.append(tax_exist.id)
                k = k + 1
        if not tax_exist:
            tax_ids = super(CfdiInvoiceAttachment, self).get_tax_from_codes(taxes, tax_type, no_imp_tras)
        return tax_ids