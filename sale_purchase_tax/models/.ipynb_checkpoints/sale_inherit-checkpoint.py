# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleInherit(models.Model):
	_inherit = 'sale.order'

	@api.constrains('order_line')
	def _check_order_line(self):
		for rec in self:
			for i in rec.order_line:
				i.tax_id = rec.partner_id.sale_tax_ids
                
    @api.onchange('order_line')
	def onchange_order_line(self):
		for rec in self:
			for i in rec.order_line:
				i.tax_id = rec.partner_id.sale_tax_ids            
