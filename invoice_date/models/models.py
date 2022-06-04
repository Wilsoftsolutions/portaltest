# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InvoiceInheritReport(models.AbstractModel):
    _name = 'report.invoice_date.invoice_report_id'
    _description = 'Product Quantity Color and size wise'

    def _get_report_values(self, docids, data=None):
        invoice = self.env['account.move'].browse((docids[0]))
        for rec in invoice:
            variant_values = []
            done_ids = []
            for i in rec.invoice_line_ids:
                try:
                    if i.product_id.product_tmpl_id:
                        if i.product_id.product_tmpl_id.id not in done_ids:
                            if i.product_id.id not in done_ids:
                                if i.product_id.product_tmpl_id:
                                    product_template_id = i.product_id.product_tmpl_id.id
                                    all_same_products = self.env['product.product'].search(
                                        [('product_tmpl_id', '=', product_template_id)])
                                    color_ids_to_keep = []
                                    all_selected_color_ids = rec.invoice_line_ids.product_id.product_template_attribute_value_ids
                                    if all_selected_color_ids:
                                        for c_id in all_selected_color_ids:
                                            if c_id.attribute_id.name.upper() == 'COLOR':
                                                color_ids_to_keep.append(c_id.id)
                                            else:
                                                continue
                                    attribute_to_fetch = self.env['product.attribute.value'].search(
                                        [('id', 'in', color_ids_to_keep)])
                                    for prod in all_same_products:
                                        if prod.product_template_variant_value_ids:
                                            color_id = None
                                            for attribute in prod.product_template_variant_value_ids:
                                                if attribute.attribute_id.name.upper() == 'COLOR':
                                                    if attribute.id in attribute_to_fetch.ids:
                                                        dict_exist = next(
                                                            (item for item in variant_values if item['color_id'] ==
                                                             attribute.id), None)
                                                        if not dict_exist:
                                                            variant_values.append({
                                                                'product_name': prod.name,
                                                                'color_name': attribute.name,
                                                                'color_id': attribute.id,
                                                                'qty_available': prod.qty_available,
                                                                'uom': i.product_uom_id.name if i.product_uom_id else None,
                                                                'retail_price': i.product_id.lst_price,
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
                                                            color_id = attribute.id
                                                        else:
                                                            color_id = attribute.id
                                                    else:
                                                        continue
                                                elif attribute.attribute_id.name.upper() == 'SIZE':
                                                    dict_exist = next(
                                                        (item for item in variant_values if item['color_id'] ==
                                                         color_id), None)
                                                    if dict_exist:
                                                        dict_exist['sizes'][0][attribute.name] = prod.qty_available
                                                        color_id = None
                                        else:
                                            self.create_line_without_qty(variant_values, i)
                                    done_ids.append(i.product_id.product_tmpl_id.id)
                    else:
                        self.create_line_without_qty(variant_values, i)
                except Exception as error:
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
            'qty_available': i.product_id.qty_available,
            'uom': i.product_uom_id.name if i.product_uom_id else None,
            'retail_price': i.product_id.lst_price,
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
