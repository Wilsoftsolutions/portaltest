# -*- coding: utf-8 -*-

from odoo import models


class InvoiceInheritReport(models.AbstractModel):
    _name = 'report.invoice_date.sale_delivery_report_id'
    _description = 'Sale delivery report python file'

    def _get_report_values(self, docids, data=None):
        invoice = self.env['stock.picking'].browse((docids[0]))
        for rec in invoice:
            variant_values = []
            customer = []
            for i in rec.move_ids_without_package:
                customer.append({
                    'c_name': i.partner_id.name,
                    'address': i.partner_id.street,
                    'phone': i.partner_id.phone,
                    'user': self.env.user.name,
                    'date': rec.scheduled_date,
                })
                try:
                    if i.product_id.product_tmpl_id:
                        product_attribute = i.product_id.product_template_attribute_value_ids
                        color_id = product_attribute.filtered(
                            lambda attribute: attribute.attribute_id.name.upper() == 'COLOR'
                        )
                        size = product_attribute.filtered(
                            lambda attribute: attribute.attribute_id.name.upper() == 'SIZE'
                        )
                        dict_exist = next(
                            (item for item in variant_values if item['color_id'] ==
                             color_id.id), None)
                        if not dict_exist:
                            new_dict = {
                                'product_name': i.product_id.name,
                                'color_name': color_id.name,
                                'color_id': color_id.id,
                                'uom': i.product_uom.name if i.product_uom else None,
                                'retail_price': i.price_unit,
                                'line_total_qty': 0,
                                'taxes': rec.amount_tax_signed,
                                'net_amount': rec.amount_total,
                                'sizes': [{
                                    '39': 0,
                                    '40': 0,
                                    '41': 0,
                                    '42': 0,
                                    '43': 0,
                                    '44': 0,
                                    '45': 0,
                                    '46': 0,
                                }]
                            }
                            new_dict['sizes'][0][size.name] += i.quantity
                            variant_values.append(new_dict)
                        else:
                            dict_exist['sizes'][0][size.name] += i.quantity

                    else:
                        self.create_line_without_pickage(variant_values, i)

                except Exception:
                    self.create_line_without_pickage(variant_values, i)

        return {
            'doc_model': 'stock.picking',
            'data': data,
            'c_name': rec.partner_id.name,
            'user': self.env.user.name,
            'date': rec.scheduled_date,
            'address': rec.partner_id.street,
            'phone': rec.partner_id.phone,
            'variant_values': variant_values,
        }

    def create_line_without_pickage(self, variant_values=None, i=None):
        variant_values.append({
            'product_name': i.product_id.name,
            'color_name': '-',
            'color_id': '',
            'uom': i.product_uom.name if i.product_uom else None,
            'retail_price': i.price_unit,
            'line_total_qty': i.product_uom_qty,
            'taxes': 0,
            'net_amount': 0,
            'sizes': [{
                '39': 0,
                '40': 0,
                '41': 0,
                '42': 0,
                '43': 0,
                '44': 0,
                '45': 0,
                '46': 0,
            }]
        })
        return variant_values
