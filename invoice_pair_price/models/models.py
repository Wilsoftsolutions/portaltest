# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InheritInvoiceLIne(models.Model):
	_inherit = 'account.move.line'

	x_studio_pair_price = fields.Float('Pair Price')



class InheritSaleOrderline(models.Model):
	_inherit = 'sale.order.line'

	def _prepare_invoice_line(self, **optional_values):
		# Updating discount amount (in float) on invoice line
		res = super(InheritInvoiceLIne, self)._prepare_invoice_line(**optional_values)
		for rec in self:
			if rec.x_studio_pair_price:
				res.update({'x_studio_pair_price': rec.x_studio_pair_price})
			else:
				continue
		return res


