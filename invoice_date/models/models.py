# -*- coding: utf-8 -*-

from odoo import models


class InvoiceInheritReport(models.AbstractModel):
    _name = 'report.invoice_date.invoice_report_id'
    _description = 'Product Quantity Color and size wise'

    def _get_report_values(self, docids, data=None):
        invoice = self.env['account.move'].browse((docids[0]))
        for rec in invoice:
            variant_values = []
            for i in rec.invoice_line_ids:
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
                                'uom': i.product_uom_id.name if i.product_uom_id else None,
                                'retail_price': i.price_unit,
                                'line_total_qty': 0,
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
                        self.create_line_without_qty(variant_values, i)

                except Exception:
                    self.create_line_without_qty(variant_values, i)

        return {
            'doc_model': 'account.move',
            'data': data,
            'variant_values': variant_values,
        }

    def create_line_without_qty(self, variant_values=None, i=None):
        variant_values.append({
            'product_name': i.product_id.name,
            'color_name': '-',
            'color_id': '',
            'uom': i.product_uom_id.name if i.product_uom_id else None,
            'retail_price': i.price_unit,
            'line_total_qty': i.quantity,
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
