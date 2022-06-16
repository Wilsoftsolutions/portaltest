# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class QcInspection(models.Model):
	_name = 'qc.inspection'
	_description = 'Qc Inspection'

	name = fields.Many2one('hr.employee', string='Quality Control Inspector', domain="[('job_id', '=', 'Officer QA')]")
	ref = fields.Char(string='Ref. SR# :', readonly='True')
	vendor_id = fields.Many2one('res.partner', string='Vendor Name', domain="[('category_id', '=', 'Vendor')]")
	purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order',
										domain="[('invoice_status', '=', 'no'),('partner_id', '=', ' ')]")
	po_item_id = fields.Many2one('purchase.order.line', string='Article', domain="[('order_id', '=', ' ')]")
	image = fields.Binary(string=' ', store=True)
	plan = fields.Integer(string=' ', readonly='True', store=True)
	status = fields.Char(string=' ', default='Created', readonly='True')
	article36 = fields.Integer(string=' ', readonly='True', store=True)
	article37 = fields.Integer(string=' ', readonly='True', store=True)
	article38 = fields.Integer(string=' ', readonly='True', store=True)
	article39 = fields.Integer(string=' ', readonly='True', store=True)
	article40 = fields.Integer(string=' ', readonly='True', store=True)
	article41 = fields.Integer(string=' ', readonly='True', store=True)
	article42 = fields.Integer(string=' ', readonly='True', store=True)
	article43 = fields.Integer(string=' ', readonly='True', store=True)
	article44 = fields.Integer(string=' ', readonly='True', store=True)
	article45 = fields.Integer(string=' ', readonly='True', store=True)
	article46 = fields.Integer(string=' ', readonly='True', store=True)
	check36 = fields.Integer(string=' ')
	check37 = fields.Integer(string=' ')
	check38 = fields.Integer(string=' ')
	check39 = fields.Integer(string=' ')
	check40 = fields.Integer(string=' ')
	check41 = fields.Integer(string=' ')
	check42 = fields.Integer(string=' ')
	check43 = fields.Integer(string=' ')
	check44 = fields.Integer(string=' ')
	check45 = fields.Integer(string=' ')
	check46 = fields.Integer(string=' ')
	rework36 = fields.Integer(string=' ')
	rework37 = fields.Integer(string=' ')
	rework38 = fields.Integer(string=' ')
	rework39 = fields.Integer(string=' ')
	rework40 = fields.Integer(string=' ')
	rework41 = fields.Integer(string=' ')
	rework42 = fields.Integer(string=' ')
	rework43 = fields.Integer(string=' ')
	rework44 = fields.Integer(string=' ')
	rework45 = fields.Integer(string=' ')
	rework46 = fields.Integer(string=' ')
	bpair36 = fields.Integer(string=' ')
	bpair37 = fields.Integer(string=' ')
	bpair38 = fields.Integer(string=' ')
	bpair39 = fields.Integer(string=' ')
	bpair40 = fields.Integer(string=' ')
	bpair41 = fields.Integer(string=' ')
	bpair42 = fields.Integer(string=' ')
	bpair43 = fields.Integer(string=' ')
	bpair44 = fields.Integer(string=' ')
	bpair45 = fields.Integer(string=' ')
	bpair46 = fields.Integer(string=' ')
	bal_36 = fields.Integer(string=' ', readonly='True', store=True)
	bal_37 = fields.Integer(string=' ', readonly='True', store=True)
	bal_38 = fields.Integer(string=' ', readonly='True', store=True)
	bal_39 = fields.Integer(string=' ', readonly='True', store=True)
	bal_40 = fields.Integer(string=' ', readonly='True', store=True)
	bal_41 = fields.Integer(string=' ', readonly='True', store=True)
	bal_42 = fields.Integer(string=' ', readonly='True', store=True)
	bal_43 = fields.Integer(string=' ', readonly='True', store=True)
	bal_44 = fields.Integer(string=' ', readonly='True', store=True)
	bal_45 = fields.Integer(string=' ', readonly='True', store=True)
	bal_46 = fields.Integer(string=' ', readonly='True', store=True)
	upper = fields.Char(string='Upper')
	linning = fields.Char(string='Linning')
	mid_sole = fields.Char(string='MID Sole')
	outsole = fields.Char(string='OUTSole')
	finished = fields.Char(string='Finished')
	packaging = fields.Char(string='Packaging')
	acc = fields.Char(string='Acc')
	other = fields.Char(string='Others')
	comment = fields.Text(string="Comment")
	attch_ids = fields.Many2many('ir.attachment', 'ir_attach_rel', 'record_relation_id', 'attachment_id',
								 string="Attachments",
								 help="If any")

	@api.onchange('vendor_id')
	def onchange_vendor_id(self):
		self.purchase_order_id = ''
		return {'domain': {'purchase_order_id': [('partner_id', '=', self.vendor_id.id)]}}

	@api.onchange('purchase_order_id')
	def onchange_purchase_order_id(self):
		self.po_item_id = ''
		return {'domain': {'po_item_id': [('order_id', '=', self.purchase_order_id.id)]}}

	@api.onchange('check36','check37','check38','check39','check40','check41','check42','check43','check44','check45','check46')
	def onchange_all_balance(self):
		for rec in self:
			rec.bal_36 = rec.article36 - rec.check36
			rec.bal_37 = rec.article37 - rec.check37
			rec.bal_38 = rec.article38 - rec.check38
			rec.bal_39 = rec.article39 - rec.check39
			rec.bal_40 = rec.article40 - rec.check40
			rec.bal_41 = rec.article41 - rec.check41
			rec.bal_42 = rec.article42 - rec.check42
			rec.bal_43 = rec.article43 - rec.check43
			rec.bal_44 = rec.article44 - rec.check44
			rec.bal_45 = rec.article45 - rec.check45
			rec.bal_46 = rec.article46 - rec.check46


	@api.onchange('po_item_id')
	def onchange_member_type(self):
		articl36= 0
		articl37 = 0
		articl38 = 0
		articl39 = 0
		articl40 = 0
		articl41 = 0
		articl42 = 0
		articl43 = 0
		articl44 = 0
		articl45 = 0
		articl46 = 0
		for rec in self:
			for po in rec.po_item_id:
				rec.image = po.product_id.image_1920
				for line in po.product_id.sh_bundle_product_ids:

					product_attribute = line.sh_product_id.product_template_attribute_value_ids
					size = product_attribute.filtered(
						lambda attribute: attribute.attribute_id.name.upper() == 'SIZE'
					)
					if size.name == '36':
						articl39 += line.sh_qty * po.product_qty
					if size.name == '37':
						articl39 += line.sh_qty * po.product_qty
					if size.name == '38':
						articl39 += line.sh_qty * po.product_qty
					if size.name == '39':
						articl39 += line.sh_qty * po.product_qty
					if size.name == '40':
						articl40 += line.sh_qty * po.product_qty
					if size.name == '41':
						articl41 += line.sh_qty * po.product_qty
					if size.name == '42':
						articl42 += line.sh_qty * po.product_qty
					if size.name == '43':
						articl43 += line.sh_qty * po.product_qty
					if size.name == '44':
						articl44 += line.sh_qty * po.product_qty
					if size.name == '45':
						articl45 += line.sh_qty * po.product_qty
					if size.name == '46':
						articl40 += line.sh_qty * po.product_qty
			rec.article36 = articl36
			rec.article37 = articl37
			rec.article38 = articl38
			rec.article39 = articl39
			rec.article40 = articl40
			rec.article41 = articl41
			rec.article42 = articl42
			rec.article43 = articl43
			rec.article44 = articl44
			rec.article45 = articl45
			rec.article46 = articl46



	def action_status(self):
		self.status = 'Confrimed'
