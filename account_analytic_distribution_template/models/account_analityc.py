# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError
import json


class AnalyticDistributionTemplate(models.Model):
    _name = 'account.analytic.distribution.template'
    _description = 'Plantillas de distribución analítica'
    _inherit = 'analytic.mixin'

    name = fields.Char('Nombre', required=True)
    analytic_dist_plan_ids = fields.One2many('account.analytic.distribution.plan', 'template_id', 'Planes')
    analytic_total = fields.Json('Totales', store=True, copy=False, readonly=False)
    asignado = fields.Float('Asignado', compute='_compute_asignado')
    analytic_dist_model_id = fields.Many2one('account.analytic.distribution.model', 'Modelo de Distribución')
    company_id = fields.Many2one('res.company', 'Compañía', default=lambda self: self.env.user.company_id)

    @api.depends('analytic_total')
    def _compute_asignado(self):
        if self.analytic_total:
            self.asignado = sum(self.analytic_total.values())/100
        else:
            self.asignado = 0

    def calc_distribucion_analitica(self):
        totales = {}
        dist_plan_vals = {}
        porc = 0
        for lin in self.analytic_dist_plan_ids:
            dist_plan_vals[lin.name.id] = lin.porcentaje
            porc += round(lin.porcentaje, 6)
        if porc != 1:
            raise UserError('La suma de los porcentajes no es 100%% (Actual: %s%%)'%(porc*100))
        for cuenta_str,porc in self.analytic_distribution.items():
            cuenta = self.env['account.analytic.account'].browse(int(cuenta_str))
            totales[cuenta_str] = round(porc * dist_plan_vals[cuenta.plan_id.id], 6)
        self.analytic_total = totales

    @api.onchange('analytic_distribution')
    def onchange_analytic_distribution(self):
        #import pdb;pdb.set_trace()
        if self.analytic_distribution:
            for analitica in self.analytic_distribution.keys():
                cuenta = self.env['account.analytic.account'].browse(int(analitica))
                if not self.analytic_dist_plan_ids:
                    self.write({'analytic_dist_plan_ids': [(0,0, {'name': cuenta.plan_id.id, 'porcentaje': 1})]})
                else:
                    if cuenta.plan_id.id not in self.analytic_dist_plan_ids.name.ids:
                        self.write({'analytic_dist_plan_ids': [(0, 0, {'name': cuenta.plan_id.id, 'porcentaje': 0})]})
        else:
            self.analytic_dist_plan_ids = False

    def aplicar_distribucion_analitica(self):
        if self.analytic_total and self.analytic_dist_model_id:
            self.analytic_dist_model_id.analytic_distribution = self.analytic_total


class AccountAnalyticDistributionPlan(models.Model):
    _name = 'account.analytic.distribution.plan'
    _description = 'Planes de Distribución Analítica'

    name = fields.Many2one('account.analytic.plan', 'Plan')
    porcentaje = fields.Float('Porcentaje')
    template_id = fields.Many2one('account.analytic.distribution.template', 'Plantilla')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    analytic_dist_model_id = fields.Many2one('account.analytic.distribution.model', 'Modelo de Distribución')

    def write(self, vals):
        if len(self) > 1:
            return super(AccountMoveLine, self).write(vals)
        if self.analytic_dist_model_id:
            return super(AccountMoveLine, self).write(vals)
        valores = {
            "product_id": self.product_id.id,
            "product_categ_id": self.product_id.categ_id.id,
            "partner_id": self.partner_id.id,
            "partner_category_id": self.partner_id.category_id.ids,
            "account_prefix": self.account_id.code,
            "company_id": self.company_id.id,
        }
        domain = []
        dist_model = self.env['account.analytic.distribution.model']
        for fname, value in valores.items():
            domain += dist_model._create_domain(fname, value) or []
        best_score = 0
        fnames = set(dist_model._get_fields_to_check())
        for rec in dist_model.search(domain):
            try:
                score = sum(rec._check_score(key, valores.get(key)) for key in fnames)
                if score > best_score:
                    vals['analytic_dist_model_id'] = rec.id
                    best_score = score
            except:
                continue
        vals = super(AccountMoveLine, self).write(vals)
        return vals


class AccountMove(models.Model):
    _inherit = 'account.move'

    def create(self, vals_list):
        journal_cash_id = self.env.company.tax_cash_basis_journal_id.id
        for move in vals_list:
            if move.get('journal_id') == journal_cash_id:
                try:
                    for tupla in move.get('line_ids'):
                        tupla[2].update({'analytic_distribution': False})
                except:
                    pass
        return super(AccountMove, self).create(vals_list)